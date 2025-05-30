"""An AWS Python Pulumi program"""

from pulumi_aws import s3
from infrastructure import static, network

def deploy(stage: str):

    bucket = static.bucket(stage)

    cert = network.certificate(stage)

    cdn = static.cdn(stage, bucket, network.DOMAIN_NAME, cert)

    network.cdn_alias_record(stage, cdn)

