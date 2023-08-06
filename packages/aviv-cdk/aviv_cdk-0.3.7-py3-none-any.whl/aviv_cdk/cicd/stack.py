import typing
from constructs import Construct
from aws_cdk import (
    Stack,
    Stage,
    aws_ssm,
    aws_iam,
    aws_codestarconnections,
    pipelines
)
from . import (
    sources as gh_sources
)


class CodePipelineStack(Stack):
    codepipeline: pipelines.CodePipeline
    source: pipelines.CodePipelineSource
    additional_sources: typing.Dict[str, pipelines.CodePipelineSource]={}
    connections: typing.Dict[str, aws_codestarconnections.CfnConnection]={}
    waves: typing.Dict[str, pipelines.Wave]={}
    stages: typing.Dict[str, typing.Dict[str, Stage]]={}

    def __init__(self, scope: Construct, id: str, *, connections: dict, source: dict, synthargs: dict, pipelineargs: dict={}, additional_sources: typing.Dict[str, dict]=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self._setup_sources(connections=connections, source=source, additional_sources=additional_sources)
        self.codepipeline = pipelines.CodePipeline(
            self, 'pipeline',
            self_mutation=False,
            cross_account_keys=True,
            synth=pipelines.ShellStep(
                'Synth',
                input=self.source,
                additional_inputs=self.additional_sources,
                **synthargs
            ),
            **pipelineargs
        )

    def _setup_sources(self, connections: dict, source: dict, additional_sources: typing.Dict[str, dict]=None) -> None:
        for cname, connection_ssm in connections.items():
            self.connections[cname] = aws_ssm.StringParameter.value_from_lookup(self, parameter_name=connection_ssm.replace('aws:ssm:', ''))
        self.source = pipelines.CodePipelineSource.connection(
            connection_arn=self.connections[source['repo_string'].split('/')[0]],
            **source
        )
        if not additional_sources:
            return
        for skey, additional_source in additional_sources.items():
            # sn = additional_source['repo_string'].replace('/', '_').replace('-', '_')
            owner = additional_source['repo_string'].split('/')[0]
            self.additional_sources[skey] = pipelines.CodePipelineSource.connection(
                connection_arn=self.connections[owner],
                **additional_source
            )

