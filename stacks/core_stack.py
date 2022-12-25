from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as lambda_python,
    aws_timestream as timestream,
    custom_resources,
)
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
            }
        )

        resource_provider = custom_resources.Provider(
            self,
            "custom-resource-provider",
            on_event_handler=on_event_handler
        )

        self.resource_provider = resource_provider