"""An AWS Python Pulumi program"""

import pulumi_aws as aws
from infrastructure import static, network, service
import pulumi 


def deploy(stage: str, project_name: str):

    vpc, subnets = network.vpc(stage, project_name)

    subnet_ids = [id for id in subnets]

    cert = network.certificate(stage, project_name)

    bucket = static.bucket(stage, project_name)

    cdn = static.cdn(stage, project_name, bucket, network.DOMAIN_NAME, cert)

    network.cdn_alias_record(stage, project_name, cdn)

    alb, target_group, listener = network.alb(stage, project_name, subnet_ids)

    cluster = aws.ecs.Cluster(f"{stage}-cluster-{project_name}") 

    ecr = service.ecr(stage, project_name)

    ecr_image_uri = pulumi.Output.concat(ecr.repository_url, ":latest")

    pulumi.export("ecrImageUri", ecr_image_uri)

    service.ecs(
        stage, 
        project_name,
        cluster, 
        subnet_ids, 
        target_group, 
        ecr_image_uri
    )

