import pulumi
import pulumi_aws as aws
import mimetypes
from pathlib import Path
import json

ABSOLUTE_PATH = "/workspace/decouple/static/"

def bucket(stage: str, project_name) -> aws.s3.Bucket:
    # Create the S3 bucket
    bucket = aws.s3.Bucket(
        f"{stage}-bucket-{project_name}",
        website=aws.s3.BucketWebsiteArgs(
            index_document="index.html",
            error_document="404.html",
        )
    )

    aws.s3.BucketPublicAccessBlock(
        f"{stage}-bucket-public-access-block-{project_name}",
        bucket=bucket.id,
        block_public_acls=False,
        block_public_policy=False,
        ignore_public_acls=False,
        restrict_public_buckets=False
    )

    aws.s3.BucketPolicy(
        f"{stage}-bucket-policy-{project_name}",
        bucket=bucket.id,
        policy=bucket.id.apply(lambda bucket_name: json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }]
        }))
    )

    # Upload files from source_dir to the bucket
    root_path = Path(ABSOLUTE_PATH)
    for file_path in root_path.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(root_path).as_posix()
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or "application/octet-stream"

            aws.s3.BucketObject(
                f"{stage}-{relative_path}-{project_name}",
                bucket=bucket.id,
                key=relative_path,
                source=pulumi.FileAsset(str(file_path)),
                content_type=mime_type,
            )

    # Export the bucket's website endpoint
    pulumi.export(f"{stage}_bucket_endpoint", bucket.website_endpoint)

    return bucket

def cdn(stage: str, project_name: str, bucket: aws.s3.Bucket, domain_name: str, cert: aws.acm.Certificate) -> aws.cloudfront.Distribution:
    # 1) Create a us-east-1 provider for CloudFront (CloudFront certificates must live in us-east-1)
    us_east_1 = aws.Provider(f"{stage}-us-east-1", region="us-east-1")

    # 2) Origin Access Identity for S3, using the us-east-1 provider
    oai = aws.cloudfront.OriginAccessIdentity(
        f"{stage}-cdn-oai",
        comment=f"Access identity for {stage}-{project_name} CDN",
        opts=pulumi.ResourceOptions(provider=us_east_1)
    )

    # 3) Build the CloudFront Distribution using the us-east-1 provider
    distribution = aws.cloudfront.Distribution(
        f"{stage}-cdnDistribution-{project_name}",
        origins=[aws.cloudfront.DistributionOriginArgs(
            domain_name=bucket.bucket_regional_domain_name,
            origin_id=bucket.arn,
            s3_origin_config=aws.cloudfront.DistributionOriginS3OriginConfigArgs(
                origin_access_identity=oai.cloudfront_access_identity_path,
            ),
        )],
        enabled=True,
        default_root_object="index.html",
        default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
            target_origin_id=bucket.arn,
            viewer_protocol_policy="redirect-to-https",
            allowed_methods=["GET", "HEAD"],
            cached_methods=["GET", "HEAD"],
            forwarded_values=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs(
                query_string=False,
                cookies=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesCookiesArgs(
                    forward="none"
                ),
            ),
        ),
        price_class="PriceClass_100",
        restrictions=aws.cloudfront.DistributionRestrictionsArgs(
            geo_restriction=aws.cloudfront.DistributionRestrictionsGeoRestrictionArgs(
                restriction_type="none"
            )
        ),
        aliases=[f"static.{domain_name}"],
        viewer_certificate=aws.cloudfront.DistributionViewerCertificateArgs(
            acm_certificate_arn=cert.arn,  # Certificate ARN must be from us-east-1
            ssl_support_method="sni-only",
            minimum_protocol_version="TLSv1.2_2021",
        ),
    )

    pulumi.export(f"{stage}-cdn_domain_name", distribution.domain_name)
    return distribution
