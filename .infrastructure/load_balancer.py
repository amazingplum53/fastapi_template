import pulumi
import pulumi_aws as aws
from vpc import subnets, security_group

# Create an Application Load Balancer
load_balancer = aws.lb.LoadBalancer("django-lb",
    security_groups=[security_group.id],
    subnets=subnets.ids
)

target_group = aws.lb.TargetGroup("django-tg",
    port=8000,
    protocol="HTTP",
    vpc_id=subnets.vpc_id,  # Use VPC ID from network module
    target_type="ip"
)

listener = aws.lb.Listener("django-listener",
    load_balancer_arn=load_balancer.arn,
    port=80,
    protocol="HTTP",
    default_actions=[{
        "type": "forward",
        "target_group_arn": target_group.arn
    }]
)

# Export ALB DNS
pulumi.export("load_balancer_url", load_balancer.dns_name)
