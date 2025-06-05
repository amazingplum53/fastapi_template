"""An AWS Python Pulumi program"""

import pulumi_aws as aws
from infrastructure import static, network, service
import pulumi 


def deploy(stage: str):

    subnet_ids = network.subnet_ids(stage)

    cert = network.certificate(stage)

    bucket = static.bucket(stage)

    cdn = static.cdn(stage, bucket, network.DOMAIN_NAME, cert)

    network.cdn_alias_record(stage, cdn)

    alb, target_group, listener = network.alb(stage, subnet_ids)

    cluster = aws.ecs.Cluster("django-cluster")

    ecr = service.ecr(stage, stage + "decouple")

    ecr_image_uri = pulumi.Output.concat(ecr.repository_url, ":latest")

    pulumi.export("ecrImageUri", ecr_image_uri)

    service.ecs(
        stage, 
        cluster, 
        subnet_ids, 
        target_group, 
        ecr_image_uri
    )

