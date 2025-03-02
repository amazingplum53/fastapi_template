import pulumi
import pulumi_aws as aws
import pulumi_docker as docker
from vpc import subnets, security_group

# Create an ECS Cluster
cluster = aws.ecs.Cluster("ecs-cluster")

# Define an ECR repository
ecr_repo = aws.ecr.Repository("django-ecr-repo")

# Build and push Docker image to ECR
image = docker.Image("django-app-image",
    build=docker.DockerBuildArgs(context="."),
    image_name=ecr_repo.repository_url,
    skip_push=False
)

# IAM Role for ECS Tasks
task_role = aws.iam.Role("ecs-task-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": { "Service": "ecs-tasks.amazonaws.com" },
                "Effect": "Allow"
            }
        ]
    }"""
)

aws.iam.RolePolicyAttachment("ecs-task-execution-policy",
    role=task_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
)

# Task Definition for Django
task_definition = aws.ecs.TaskDefinition("django-task",
    family="django-task",
    cpu="512",
    memory="1024",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=task_role.arn,
    container_definitions=pulumi.Output.all(image.image_name).apply(lambda img: f"""
    [
        {{
            "name": "django",
            "image": "{img}",
            "cpu": 512,
            "memory": 1024,
            "essential": true,
            "portMappings": [
                {{
                    "containerPort": 8000,
                    "hostPort": 8000
                }}
            ]
        }}
    ]
    """)
)

# Export values
pulumi.export("ecs_cluster_arn", cluster.arn)
pulumi.export("task_definition_arn", task_definition.arn)
