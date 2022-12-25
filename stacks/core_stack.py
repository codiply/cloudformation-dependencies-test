from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as lambda_python,
    aws_timestream as timestream,
    custom_resources,
)
import aws_cdk as cdk
from constructs import Construct

class CoreStack(Stack):

    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        prefix: str, 
        **kwargs) -> None:
        
        super().__init__(scope, construct_id, **kwargs)

        database_name = f"{prefix}-timestream"
        table_name = f"{prefix}-measurements"

        database =timestream.CfnDatabase(
            self,
            "timestream-database",
            database_name=database_name
        )

        table = timestream.CfnTable(
            self,
            "timestream-table",
            database_name=database_name,
            table_name=table_name
        )
        table.node.add_dependency(database)

        on_event_handler_role = iam.Role(
            self,
            "on-event-handler-role",
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    'service-role/AWSLambdaBasicExecutionRole')
            ],
            inline_policies={
                'AllowWriteToTimestream': iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "timestream:DescribeEndpoints"
                            ],
                            resources=[
                                "*"
                            ]
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "timestream:WriteRecords"
                            ],
                            resources=[
                                (
                                    f"arn:aws:timestream:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:"
                                    f"database/{database_name}/table/{table_name}"
                                )
                            ]
                        )
                    ]
                )
            }
        )
        

        on_event_handler = lambda_python.PythonFunction(
            self,
            "resource-provider-on-event-handler",
            entry='./assets/custom-resource-provider-lambda/',
            index='handler.py',
            handler='on_event',
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={
                "DATABASE_NAME": database_name,
                "TABLE_NAME": table_name
            },
            role=on_event_handler_role
        )

        resource_provider = custom_resources.Provider(
            self,
            "custom-resource-provider",
            on_event_handler=on_event_handler
        )

        self.resource_provider_service_token = resource_provider.service_token