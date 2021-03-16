.DEFAULT: help
help:
	@echo "make cdk-deploy"
	@echo " -- deploys the cdk stack --"

cdk-synth:
	cdk synth

cdk-deploy:
	cdk bootstrap
	cdk deploy deploymentPipeline \
		--require-approval never

build-deploy:
	cdk bootstrap
	cdk deploy imagebuilder \
		--require-approval never