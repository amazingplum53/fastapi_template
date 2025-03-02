import pulumi
from vpc import subnets, security_group
from ecs import cluster, task_definition
from load_balancer import load_balancer, target_group
import pulumi_aws as aws

# Create ECS Service
ecs_service = aws.ecs.Service("django-service",
    cluster=cluster.arn,
    task_definition=task_definition.arn,
    desired_count=1,
    launch_type="FARGATE",
    network_configuration={
        "assign_public_ip": True,
        "security_groups": [security_group.id],
        "subnets": subnets.ids
    },
    load_balancers=[{
        "target_group_arn": target_group.arn,
        "container_name": "django",
        "container_port": 8000
    }]
)

# Export the ALB URL
pulumi.export("app_url", load_balancer.dns_name)
