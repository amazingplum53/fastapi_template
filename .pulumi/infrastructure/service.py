import pulumi
import pulumi_aws as aws
import json
from pulumi import Output
from typing import List, Dict


def ecs(
    stage: str,
    project_name,
    cluster: aws.ecs.Cluster,
    subnets: List[str],
    target_group: aws.lb.TargetGroup,
    ecr_image: pulumi.Input[str],
    env_vars: List[Dict[str, pulumi.Input[str]]] = [],
) -> Dict[str, pulumi.Resource]:

    # 1) Task execution IAM Role
    task_execution_role = aws.iam.Role(
        f"{stage}-exec-role-{project_name}",
        assume_role_policy=aws.iam.get_policy_document(
            statements=[{
                "actions": ["sts:AssumeRole"],
                "principals": [{
                    "type": "Service",
                    "identifiers": ["ecs-tasks.amazonaws.com"],
                }],
                "effect": "Allow",
                "sid": "",
            }]
        ).json,
    )

    aws.iam.RolePolicyAttachment(
        f"{stage}-exec-attach-{project_name}",
        role=task_execution_role.name,
        policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
    )

    # 2) Prepare to assemble container_definitions without embedding any raw Output into json.dumps()
    #    We know ecr_image: Input[str] and env_vars[i]["value"]: Input[str].
    #
    #    Extract all of the "value" fields from env_vars. These may be plain str or Output[str].
    env_values: List[pulumi.Input[str]] = [v["value"] for v in env_vars]

    #    Build a single Output that waits for ecr_image + all env_values to resolve to plain strings:
    all_inputs = Output.all(ecr_image, *env_values)

    container_name = f"{stage}-server-{project_name}"

    container_defs = all_inputs.apply(lambda args: json.dumps([{
        "name": container_name,
        "image": args[0],  # resolved ecr_image string
        "portMappings": [
            {"containerPort": 8000}
        ],
        "essential": True,
        "environment": [
            {
                "name": env_vars[i]["name"],
                "value": args[i + 1],  # resolved value for each env var
            }
            for i in range(len(env_vars))
        ],
        # You can add "logConfiguration", "healthCheck", etc., here if needed
    }]))

    # 3) Task Definition
    task_definition = aws.ecs.TaskDefinition(
        f"{stage}-task-def-{project_name}",
        family                   = f"{stage}-family-{project_name}",
        cpu                      = "512",
        memory                   = "1024",
        network_mode             = "awsvpc",
        requires_compatibilities = ["FARGATE"],
        execution_role_arn       = task_execution_role.arn,
        container_definitions    = container_defs,  # Output[str] of the JSON array above
    )

    # 4) ECS Service, using Fargate and the provided ALB Target Group
    service = aws.ecs.Service(
        f"{stage}-service-{project_name}",
        cluster         = cluster.arn,
        task_definition = task_definition.arn,
        desired_count   = 1,
        launch_type     = "FARGATE",
        network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
            assign_public_ip = True,
            subnets          = subnets,
            security_groups  = [],  # If you have a SG, put its ID here instead of an empty list
        ),
        load_balancers=[aws.ecs.ServiceLoadBalancerArgs(
            target_group_arn = target_group.arn,
            container_name   = container_name,
            container_port   = 8000,
        )],
        opts=pulumi.ResourceOptions(depends_on=[task_definition]),
    )

    # 5) Return a dict of resources in case callers want them
    return {
        "task_execution_role": task_execution_role,
        "task_definition":     task_definition,
        "service":             service,
    }


def ecr(stage, project_name):

    repo = aws.ecr.Repository(
        f"{stage}-{project_name}",
        name = f"{stage}-{project_name}",

        image_scanning_configuration = aws.ecr.RepositoryImageScanningConfigurationArgs(
            scan_on_push = True,
        ),
        tags = {
            "Environment": stage,
            "Name":        f"{stage}-{project_name}",
        }
    )

    lifecycle_policy_json = json.dumps({
        "rules": [
            {
                "rulePriority":       1,
                "description":        "Keep only last 10 images",
                "selection": {
                    "tagStatus":      "any",
                    "countType":      "imageCountMoreThan",
                    "countNumber":    10
                },
                "action": {
                    "type": "expire"
                }
            }
        ]
    })

    lifecycle = aws.ecr.LifecyclePolicy(
        f"{stage}-{project_name}-lifecycle",
        repository = repo.name,         # e.g. "prod-decouple"
        policy     = lifecycle_policy_json,
    )

    return repo
