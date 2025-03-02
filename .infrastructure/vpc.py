import pulumi
import pulumi_aws as aws

# Get the default VPC
vpc = aws.ec2.get_vpc(default=True)
subnets = aws.ec2.get_subnets(filters=[{"name": "vpc-id", "values": [vpc.id]}])

# Create a Security Group for the ECS service
security_group = aws.ec2.SecurityGroup("ecs-security-group",
    vpc_id=vpc.id,
    ingress=[{
        "protocol": "tcp",
        "from_port": 80,
        "to_port": 80,
        "cidr_blocks": ["0.0.0.0/0"],
    }],
    egress=[{
        "protocol": "-1",
        "from_port": 0,
        "to_port": 0,
        "cidr_blocks": ["0.0.0.0/0"],
    }]
)

# Export values for use in other modules
pulumi.export("vpc_id", vpc.id)
pulumi.export("subnet_ids", subnets.ids)
pulumi.export("security_group_id", security_group.id)
