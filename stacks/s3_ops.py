import os

from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment
)


class S3Ops(core.Stack):

    def __init__(self, scope: core.Construct, id: str, bucket_name: str, components_prefix: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create an s3 bucket
        ops_bucket = s3.Bucket(self,
                               "stack_ops_bucket",
                               bucket_name=bucket_name,
                               versioned=True
                               )

        # set component folder as source for deployment
        source_asset = s3_deployment.Source.asset('./components')

        # deploy everything under folder to s3 bucket
        s3_deployment.BucketDeployment(self,
                                       "stacks_components_deployment",
                                       destination_bucket=ops_bucket,
                                       sources=[source_asset],
                                       destination_key_prefix=components_prefix
                                       )
