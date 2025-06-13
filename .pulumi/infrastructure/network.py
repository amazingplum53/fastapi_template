import pulumi_aws as aws
import pulumi

DOMAIN_NAME = "matthewhill.click"


def vpc(stage, project_name):

    azs = aws.get_availability_zones()

    vpc = aws.ec2.Vpc(
        f"{stage}-vpc-{project_name}",
        cidr_block="10.0.0.0/16",
        enable_dns_hostnames=True,
        enable_dns_support=True,
        tags={"Name": "pulumi-two-az-vpc"},
    )

    # 4) Create an Internet Gateway so our subnets can be public
    igw = aws.ec2.InternetGateway(
        f"{stage}-igw-{project_name}",
        vpc_id=vpc.id,
        tags={"Name": "pulumi-vpc-igw"},
    )

    # 5) Make a single public route table for the VPC
    public_route_table = aws.ec2.RouteTable(
        f"{stage}-publicRT-{project_name}",
        vpc_id=vpc.id,
        routes=[
            aws.ec2.RouteTableRouteArgs(
                cidr_block="0.0.0.0/0",
                gateway_id=igw.id,
            ),
        ],
        tags={"Name": "pulumi-public-rt"},
    )

    # 6) Create two public subnets in two different AZs
    public_subnet_a = aws.ec2.Subnet(
        f"{stage}-publicSubnetA-{project_name}",
        vpc_id=vpc.id,
        cidr_block="10.0.1.0/24",
        availability_zone=azs.names[0],
        map_public_ip_on_launch=True,
        tags={"Name": pulumi.Output.concat("pulumi-public-subnet-", azs.names[0])},
    )

    public_subnet_b = aws.ec2.Subnet(
        f"{stage}-publicSubnetB-{project_name}",
        vpc_id=vpc.id,
        cidr_block="10.0.2.0/24",
        availability_zone=azs.names[1],
        map_public_ip_on_launch=True,
        tags={"Name": pulumi.Output.concat("pulumi-public-subnet-", azs.names[1])},
    )

    # 7) Associate both subnets with the public route table
    rta_a = aws.ec2.RouteTableAssociation(
        f"{stage}-rtaA-{project_name}",
        subnet_id=public_subnet_a.id,
        route_table_id=public_route_table.id,
    )

    rta_b = aws.ec2.RouteTableAssociation(
        f"{stage}-rtaB-{project_name}",
        subnet_id=public_subnet_b.id,
        route_table_id=public_route_table.id,
    )

    return [
        vpc,
        [public_subnet_a, public_subnet_b]
    ]


def cdn_alias_record(stage: str, project_name, cdn: aws.cloudfront.Distribution) -> aws.route53.Record:

    hosted_zone = aws.route53.get_zone(name=DOMAIN_NAME)

    record = aws.route53.Record(
        f"{stage}-cdnAliasRecord-{project_name}",
        zone_id=hosted_zone.zone_id,
        name = "static." + DOMAIN_NAME,
        type="A",
        aliases=[aws.route53.RecordAliasArgs(
            name=cdn.domain_name,
            zone_id="Z2FDTNDATAQYW2",
            evaluate_target_health=False,
        )]
    )
    return record


def certificate(stage: str, project_name) -> aws.acm.Certificate:
    # Create AWS provider for us-east-1 region (required by ACM)
    us_east_1_provider = aws.Provider("usEast1", region="us-east-1")

    cert = aws.acm.Certificate(
        f"{stage}-cdnCertificate-{project_name}",
        domain_name=f"static.{DOMAIN_NAME}",
        validation_method="DNS",
        opts=pulumi.ResourceOptions(provider=us_east_1_provider),
    )

    # Set up DNS validation record in Route 53
    zone = aws.route53.get_zone(name=DOMAIN_NAME)

    validation_record = aws.route53.Record(
        f"{stage}-certValidationRecord-{project_name}",
        zone_id=zone.zone_id,
        name=cert.domain_validation_options[0].resource_record_name,
        type=cert.domain_validation_options[0].resource_record_type,
        records=[cert.domain_validation_options[0].resource_record_value],
        ttl=60,
        opts=pulumi.ResourceOptions(provider=us_east_1_provider),
    )

    cert_validation = aws.acm.CertificateValidation(
        f"{stage}-certValidation-{project_name}",
        certificate_arn=cert.arn,
        validation_record_fqdns=[validation_record.fqdn],
        opts=pulumi.ResourceOptions(provider=us_east_1_provider),
    )

    pulumi.export("Certificate", cert.id)
    pulumi.export("CertificateValidation", cert_validation.id)

    return cert


def alb(stage: str, project_name: str, subnet_ids: pulumi.Input[list]) -> tuple:

    first_subnet = aws.ec2.get_subnet_output(id=subnet_ids[0])

    alb = aws.lb.LoadBalancer(
        f"{stage}-alb-{project_name}",
        internal=False,
        load_balancer_type="application",
        security_groups=[],  # Add your SG IDs here if needed
        subnets=subnet_ids,
    )

    target_group = aws.lb.TargetGroup(
        f"{stage}-tg-{project_name}",
        port=8000,
        protocol="HTTP",
        target_type="ip",
        vpc_id=first_subnet.vpc_id,  # Use VPC ID from the first subnet
        health_check=aws.lb.TargetGroupHealthCheckArgs(
            path="/health",
            interval=30,
            timeout=5,
            healthy_threshold=2,
            unhealthy_threshold=2,
        ),
    )

    listener = aws.lb.Listener(
        f"{stage}-listener-{project_name}",
        load_balancer_arn=alb.arn,
        port=80,
        protocol="HTTP",  # Must specify protocol
        default_actions=[aws.lb.ListenerDefaultActionArgs(
            type="forward",
            target_group_arn=target_group.arn,
        )],
    )

    pulumi.export(f"{stage}_alb_dns", alb.dns_name)

    return alb, target_group, listener


