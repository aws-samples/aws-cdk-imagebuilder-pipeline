import os

from aws_cdk import (
    core,
    aws_imagebuilder as imagebuilder,
    aws_iam as iam
)


class AwsCfImagebuilderPipeline(core.Stack):

    def __init__(self, scope: core.Construct, id: str, bucket_name: str, components_prefix: str, base_image_arn: str,
                 image_pipeline_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_uri = "s3://" + bucket_name + "/" + components_prefix

        # NOTE: when creating components, version number is supplied manually. If you update the components yaml and
        # need a new version deployed, version need to be updated manually.

        # spec to install python3
        component_python3_uri = bucket_uri + '/install_python3.yml'
        component_python3 = imagebuilder.CfnComponent(self,
                                                      "component_python3",
                                                      name="InstallPython3",
                                                      platform="Linux",
                                                      version="1.0.1",
                                                      uri=component_python3_uri
                                                      )

        # spec to install angular
        component_angular_uri = bucket_uri + '/install_angular.yml'
        component_angular = imagebuilder.CfnComponent(self,
                                                      "component_angular",
                                                      name="InstallAngular",
                                                      platform="Linux",
                                                      version="1.0.0",
                                                      uri=component_angular_uri
                                                      )

        # spec to install dotnet core
        component_dotnet_uri = bucket_uri + '/install_dotnetcore.yml'
        component_dotnet = imagebuilder.CfnComponent(self,
                                                     "component_dotnet",
                                                     name="InstallDotnetCore",
                                                     platform="Linux",
                                                     version="1.0.0",
                                                     uri=component_dotnet_uri
                                                     )

        # spec to install docker and other dev tools
        component_devtools_uri = bucket_uri + '/install_devtools.yml'
        component_devtools = imagebuilder.CfnComponent(self,
                                                       "component_devtools",
                                                       name="InstallDevTools",
                                                       platform="Linux",
                                                       version="1.0.0",
                                                       uri=component_devtools_uri
                                                       )

        # recipe that installs all of above components together with a ubuntu base image
        recipe = imagebuilder.CfnImageRecipe(self,
                                             "UbuntuDevWorkstationRecipe",
                                             name="UbuntuDevWorkstationRecipe",
                                             version="1.0.3",
                                             components=[
                                                 {"componentArn": component_python3.attr_arn},
                                                 {"componentArn": component_angular.attr_arn},
                                                 {"componentArn": component_dotnet.attr_arn},
                                                 {"componentArn": component_devtools.attr_arn}
                                             ],
                                             parent_image=base_image_arn
                                             )

        # below role is assumed by ec2 instance
        role = iam.Role(self, "UbuntuDevWorkstationRole", role_name="UbuntuDevWorkstationRole",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("EC2InstanceProfileForImageBuilder"))

        # create an instance profile to attach the role
        instanceprofile = iam.CfnInstanceProfile(self,
                                                 "UbuntuDevWorkstationInstanceProfile",
                                                 instance_profile_name="UbuntuDevWorkstationInstanceProfile",
                                                 roles=["UbuntuDevWorkstationRole"])

        # create infrastructure configuration to supply instance type
        infraconfig = imagebuilder.CfnInfrastructureConfiguration(self,
                                                                  "UbuntuDevWorkstationInfraConfig",
                                                                  name="UbuntuDevWorkstationInfraConfig",
                                                                  instance_types=["t3.xlarge"],
                                                                  instance_profile_name="UbuntuDevWorkstationInstanceProfile"
                                                                  )

        # infrastructure need to wait for instance profile to complete before beginning deployment.
        infraconfig.add_depends_on(instanceprofile)

        # build the imagebuilder pipeline
        pipeline = imagebuilder.CfnImagePipeline(self,
                                                 "UbuntuDevWorkstationPipeline",
                                                 name=image_pipeline_name,
                                                 image_recipe_arn=recipe.attr_arn,
                                                 infrastructure_configuration_arn=infraconfig.attr_arn
                                                 )

        pipeline.add_depends_on(infraconfig)
