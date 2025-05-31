import pulumi
import pulumi_aws as aws
import json


def ecs(
    stage: str,
    cluster: aws.ecs.Cluster,
    subnets: list[str],
    target_group: aws.lb.TargetGroup,
    ecr_image: str,
    env_vars: list[dict] = [],
) -> dict:

    # Task execution role
    task_execution_role = aws.iam.Role(f"{stage}-exec-role",
        assume_role_policy=aws.iam.get_policy_document(
            statements=[{
                "actions": ["sts:AssumeRole"],
                "principals": [{"type": "Service", "identifiers": ["ecs-tasks.amazonaws.com"]}],
            }]
        ).json,
    )

    aws.iam.RolePolicyAttachment(f"{stage}-exec-attach",
        role=task_execution_role.name,
        policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
    )

    # Task Definition
    task_definition = aws.ecs.TaskDefinition(f"{stage}-task-def",
        family=f"{stage}-family",
        cpu="512",
        memory="1024",
        network_mode="awsvpc",
        requires_compatibilities=["FARGATE"],
        execution_role_arn=task_execution_role.arn,
        container_definitions=pulumi.Output.all().apply(
            lambda _: json.dumps([{
                "name": stage,
                "image": ecr_image,
                "portMappings": [{"containerPort": 8000}],
                "essential": True,
                "environment": env_vars,
            }])
        ),
    )

    # ECS Service
    service = aws.ecs.Service(f"{stage}-service",
        cluster=cluster.arn,
        task_definition=task_definition.arn,
        desired_count=1,
        launch_type="FARGATE",
        network_configuration={
            "assign_public_ip": True,
            "subnets": subnets,
            "security_groups": [],  # Add SG IDs here
        },
        load_balancers=[{
            "target_group_arn": target_group.arn,
            "container_name": stage,
            "container_port": 8000,
        }],
    )

    return {
        "service": service,
        "task_definition": task_definition,
        "task_execution_role": task_execution_role,
    }
