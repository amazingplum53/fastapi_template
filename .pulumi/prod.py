"""An AWS Python Pulumi program"""

import pulumi_aws as aws
from infrastructure import static, network, service

def deploy(stage: str):

    cert = network.certificate(stage)

    bucket = static.bucket(stage)

    cdn = static.cdn(stage, bucket, network.DOMAIN_NAME, cert)

    network.cdn_alias_record(stage, cdn)

    alb, target_group, listener = network.alb(stage)

    cluster = aws.ecs.Cluster("django-cluster")

    ecr_repo = aws.ecr.get_repository(name="decouple")

    ecr_image_uri = f"{ecr_repo.repository_url}:latest"

    service.ecs(
        stage, 
        cluster, 
        network.subnets, 
        target_group, 
        ecr_image_uri
    )

