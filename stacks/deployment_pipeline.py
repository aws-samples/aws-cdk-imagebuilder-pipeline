from aws_cdk import (core,
                     aws_codebuild as codebuild,
                     aws_codecommit as codecommit,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_iam as iam)


class DeploymentPipeline(core.Stack):

    def __init__(self, scope: core.Construct, id: str, code_commit_repo: str, default_branch: str = 'mainline',
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        code = codecommit.Repository.from_repository_name(self, "codecommitrepo", code_commit_repo)

        # Cloudformation permission for project builds
        # right now setting admin permission on policy
        # modify this to load custom policy per pipeline from policy statement document
        # iam_cfn_admin_json = Policies.get_iam_cfn_admin_access_policy()
        policy_statement = iam.PolicyStatement()
        policy_statement.add_actions("*")
        policy_statement.add_resources("*")
        policy_statement.effect = iam.Effect.ALLOW

        serverless_build = codebuild.PipelineProject(self, "buildpipeline")

        # add cfn iam statements to build project
        serverless_build.add_to_role_policy(policy_statement)

        build_output = codepipeline.Artifact("BuildOutput")

        codepipeline.Pipeline(self, "imageBuilderDeploymentPipeline",
                              pipeline_name="ImageBuilderDeploymentPipeline",
                              stages=[
                                  codepipeline.StageProps(stage_name="Source",
                                                          actions=[
                                                              codepipeline_actions.CodeCommitSourceAction(
                                                                  action_name="SourceCode",
                                                                  branch=default_branch,
                                                                  repository=code,
                                                                  output=build_output)
                                                          ]),
                                  codepipeline.StageProps(stage_name="Deploy",
                                                          actions=[
                                                              codepipeline_actions.CodeBuildAction(
                                                                  action_name="CodeDeploy",
                                                                  project=serverless_build,
                                                                  input=build_output)
                                                          ])
                              ]
                              )
