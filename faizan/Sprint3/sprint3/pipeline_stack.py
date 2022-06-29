from aws_cdk import (
    Stack,
    pipelines as pipeline_,
    aws_codepipeline_actions as actions_,
)
import aws_cdk as cdk
from constructs import Construct
from sprint3.pipeline_stage import FaizanOutputStage

class FaizanPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Access the CommitId of a GitHub source in the synth
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipelineSource.html
        # Create Secret Token
        # https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/create-secret.html
        source = pipeline_.CodePipelineSource.git_hub("muhammadfaizan2022skipq/Pegasus_Python", "main",
            authentication = cdk.SecretValue.secrets_manager("mytokenNew"),
            trigger = actions_.GitHubTrigger('POLL'))

        unit_test = pipeline_.ShellStep("Unit",
            commands=['cd faizan/Sprint3', 'sudo apt install python-pytest'],
            primary_output_directory = 'faizan/Sprint3/cdk.out',)

        # Output build Artifact
        mypipeline = pipeline_.CodePipeline(self, "FaizanPipeline",
            synth=pipeline_.ShellStep("Synth",
                input=source,
                commands=['cd faizan/Sprint3', 'pip install -r requirements.txt', 'cdk synth'],
                primary_output_directory = 'faizan/Sprint3/cdk.out',
            )
        )

        # 'MyApplication' is defined below. Call `addStage` as many times as
        # necessary with any account and region (may be different from the
        # pipeline's).

        alpha = FaizanOutputStage(self, "FaizanUnitStage")
                
        prod = FaizanOutputStage(self, "FaizanProdStage")

        mypipeline.add_stage(stage=alpha, pre=[unit_test])
        mypipeline.add_stage(stage=prod, pre=[pipeline_.ManualApprovalStep("PromoteToProd")])
