#!/usr/bin/env python3
import configparser

from aws_cdk import core

from stacks.imagebuilder_pipeline import AwsCfImagebuilderPipeline
from stacks.s3_ops import S3Ops
from stacks.deployment_pipeline import DeploymentPipeline

config = configparser.ConfigParser()
config.read('parameters.properties')

app = core.App()

param_aws_region = config['DEFAULT']['awsRegion']

# AWS bucket where component configurations will be stored.
param_bucket_name = config['DEFAULT']['componentBucketName']

# Arn for base image that will be used to build developer workstation
# Example: "arn:aws:imagebuilder:us-west-2:aws:image/ubuntu-server-18-lts-x86/2020.8.10"
param_base_image_arn = config['DEFAULT']['baseImageArn']

# Code commit repo name on which CI pipeline need to be setup
param_code_commit_repo = config['DEFAULT']['codeCommitRepoName']

# imagebuilder pipeline will be built with this name
param_image_pipeline = config['DEFAULT']['imagePipelineName']

# s3 prefix/key for storing components
components_prefix = "components"

deploy_environment = core.Environment(region=param_aws_region)

# creates s3 bucket to store all components used in recipe
s3ops_stack = S3Ops(app,
                    "s3ops",
                    bucket_name=param_bucket_name,
                    components_prefix=components_prefix,
                    env=deploy_environment)

# builds the image builder pipeline
AwsCfImagebuilderPipeline(app,
                          "imagebuilder",
                          bucket_name=param_bucket_name,
                          components_prefix=components_prefix,
                          base_image_arn=param_base_image_arn,
                          image_pipeline_name=param_image_pipeline,
                          env=deploy_environment).add_dependency(s3ops_stack)

# a ci deployment pipeline is created only if source code is part of codecommit and repo details are supplied as
# parameters
DeploymentPipeline(app,
                   "deploymentPipeline",
                   code_commit_repo=param_code_commit_repo,
                   env=deploy_environment)

app.synth()
