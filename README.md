## ImageBuilder Pipeline using AWS CDK

This sample will create a EC2 Image builder pipeline using CDK and setup CI using code pipeline.

### Getting Started

- For setting up CDK follow instructions under "CDK Instructions".
- Create a CodeCommit repository and push the code repo to the newly created repository.
    - By default CodeCommit will create a branch named mainline, by default CI will be triggered on this branch.
    - If you choose to use a different branch (ex. dev), follow instructions below to pass it as a parameter for CI setup
        - Add a property in parameters.properties file
        ```
            codeRepoBranchName=dev
        ```
        - Pass the value as parameter to deployment stack in app.py
        ```
            param_branch_name = config['DEFAULT']['codeRepoBranchName']
            DeploymentPipeline(app,
                   "deploymentPipeline",
                   code_commit_repo=param_code_commit_repo,
                   default_branch=param_branch_name
                   env=deploy_environment)
        ```
- Update parameters.properties with appropriate values
    - componentBucketName - Bucket name where all components will be stored, this bucket will be created.
    - imagePipelineName - Name for image pipeline
    - awsRegion - AWS region in which this deployment will be done
    - baseImageArn - Ubuntu base image ARN to use ex. arn:aws:imagebuilder:us-west-2:aws:image/ubuntu-server-18-lts-x86/2020.8.10
    - codeCommitRepoName - Name of the newly created imagebuilder repo ex. mycdkubuntuimagebuilderrepo
    - Ensure parameter store values are set (refer buildspec for more details).
- Deploy deploymentpipeline stack once above step is complete to setup CI
    ```
    $ make cdk-deploy
    ```
- Once deployment of 'deploymentPipeline' stack is complete CI will deploy imagebuilder pipeline.
- Deploy imagebuilder stack from your developer workstation (use this if you skipped above steps or want to do local deployment)
    ```
    $ make build-deploy
    ```
- Imagebuilder stack can be triggered through cli using:
    ```
    $ aws imagebuilder start-image-pipeline-execution \
            --image-pipeline-arn arn:aws:imagebuilder:<<aws_region>>:<<account_number>>:image-pipeline/<<name_of_pipeline>>
    ```

### CDK Instructions

The `cdk.json` file tells the CDK Toolkit how to execute this app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth (stackname - refer stack documentation to understand which one to use)
```

If you are using MAKEFILE you can synthesize the CloudFormation template for this code.

```
$ make cdk-synth
```

If you are using MAKEFILE you can initiate an imagebuilder pipeline deployment ***with auto approval*** 

```
$ make build-deploy
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

