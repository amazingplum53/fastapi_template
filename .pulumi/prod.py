"""An AWS Python Pulumi program"""

import pulumi_aws as aws
from infrastructure import static, network, service
import pulumi 

PROJECT_ROOT = "/workspace/decouple/"


def deploy(stage: str, project_name: str):

    VPC, SUBNETS = network.vpc(stage, project_name)

    SUBNET_IDS = [id for id in SUBNETS]

    CERTIFICATE = network.certificate(stage, project_name)

    BUCKET = static.bucket(stage, project_name)

    CDN = static.cdn(stage, project_name, BUCKET, network.DOMAIN_NAME, CERTIFICATE)

    network.cdn_alias_record(stage, project_name, CDN)

    ALB, TARGET_GROUP, LISTENER = network.alb(stage, project_name, SUBNET_IDS)

    CLUSTER = aws.ecs.Cluster(f"{stage}-cluster-{project_name}") 

    ECR, IMAGE = service.ecr(stage, project_name, PROJECT_ROOT)

    ecr_image_uri = pulumi.Output.concat(ECR.repository_url, ":latest")

    TASK_EXE_ROLE, TASK_DEF, CONTAINER_SERVICE = service.ecs(
        stage, 
        project_name,
        CLUSTER, 
        VPC,
        SUBNET_IDS, 
        TARGET_GROUP, 
        ecr_image_uri
    )

