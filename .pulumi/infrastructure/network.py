import pulumi_aws as aws
import pulumi

DOMAIN_NAME = "matthewhill.click"

hosted_zone = aws.route53.get_zone(name=DOMAIN_NAME)
vpc = aws.ec2.get_vpc(default=True)
subnets = aws.ec2.get_subnets(filters=[{"name": "vpc-id", "values": [vpc.id]}])


def cdn_alias_record(stage: str, cdn: aws.cloudfront.Distribution, hosted_zone) -> aws.route53.Record:

    record = aws.route53.Record(
        "cdnAliasRecord",
        zone_id=hosted_zone.zone_id,
        name = "static." + DOMAIN_NAME,  # or "www.example.com" if you want a subdomain
        type="A",
        aliases=[aws.route53.RecordAliasArgs(
            name=cdn.domain_name,
            zone_id="Z2FDTNDATAQYW2",  # CloudFront Hosted Zone ID (fixed)
            evaluate_target_health=False,
        )]
    )
    return record


def certificate(stage: str) -> aws.acm.Certificate:
    # Create AWS provider for us-east-1 region (required by ACM)
    us_east_1_provider = aws.Provider("usEast1", region="us-east-1")

    cert = aws.acm.Certificate(
        "cdnCertificate",
        domain_name=f"static.{DOMAIN_NAME}",
        validation_method="DNS",
        opts=pulumi.ResourceOptions(provider=us_east_1_provider),
    )

    # Set up DNS validation record in Route 53
    zone = aws.route53.get_zone(name=DOMAIN_NAME)

    validation_record = aws.route53.Record(
        "certValidationRecord",
        zone_id=zone.zone_id,
        name=cert.domain_validation_options[0].resource_record_name,
        type=cert.domain_validation_options[0].resource_record_type,
        records=[cert.domain_validation_options[0].resource_record_value],
        ttl=60,
        opts=pulumi.ResourceOptions(provider=us_east_1_provider),
    )

    cert_validation = aws.acm.CertificateValidation(
        "certValidation",
        certificate_arn=cert.arn,
        validation_record_fqdns=[validation_record.fqdn],
        opts=pulumi.ResourceOptions(provider=us_east_1_provider),
    )

    pulumi.export("Certificate", cert.id)
    pulumi.export("CertificateValidation", cert_validation.id)

    return cert


def alb(stage: str, subnets: list[str]) -> tuple:
    alb = aws.lb.LoadBalancer(f"{stage}-alb",
        internal=False,
        load_balancer_type="application",
        security_groups=[],  # Add SG IDs here
        subnets=subnets,
    )

    target_group = aws.lb.TargetGroup(f"{stage}-tg",
        port=8000,
        protocol="HTTP",
        target_type="ip",
        vpc_id=vpc.id,
        health_check={
            "path": "/health",
            "interval": 30,
            "timeout": 5,
            "healthy_threshold": 2,
            "unhealthy_threshold": 2,
        }
    )

    listener = aws.lb.Listener(f"{stage}-listener",
        load_balancer_arn=alb.arn,
        port=80,
        default_actions=[{
            "type": "forward",
            "target_group_arn": target_group.arn,
        }],
    )

    pulumi.export(f"{stage}_alb_dns", alb.dns_name)

    return (
        alb,
        target_group,
        listener,
    )

