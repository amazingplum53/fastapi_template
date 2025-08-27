"""An AWS Python Pulumi program"""

import pulumi_aws as aws
from infrastructure import static, network, service
import pulumi 

def deploy(stage: str, project_name: str):

    PROJECT_ROOT = f"/workspace/{project_name}/"

    VPC, PUBLIC_SUBNETS, PRIVATE_SUBNETS = network.vpc(stage, project_name)

    PUBLIC_SUBNET_IDS = [s.id for s in PUBLIC_SUBNETS]
    PRIVATE_SUBNET_IDS = [s.id for s in PRIVATE_SUBNETS]

    CERTIFICATE = network.cdn_certificate(stage, project_name)

    BUCKET = static.bucket(stage, project_name)

    CDN = static.cdn(stage, project_name, BUCKET, network.DOMAIN_NAME, CERTIFICATE)

    network.cdn_alias_record(stage, project_name, CDN)

    ALB, TARGET_GROUP, LISTENER, SG_GROUP = network.alb(stage, project_name, PUBLIC_SUBNET_IDS)

    network.alb_alias_record(stage, project_name, ALB)

    CLUSTER = aws.ecs.Cluster(f"{stage}-cluster-{project_name}") 

    ECR, IMAGE = service.ecr(stage, project_name, PROJECT_ROOT)

    TASK_EXE_ROLE, TASK_DEF, CONTAINER_SERVICE = service.ecs(
        stage, 
        project_name,
        CLUSTER, 
        VPC,
        PRIVATE_SUBNET_IDS, 
        TARGET_GROUP, 
        IMAGE,
        SG_GROUP,
    )

