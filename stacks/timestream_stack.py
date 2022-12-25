from aws_cdk import (
    # Duration,
    Stack,
    aws_timestream as timestream
)
from constructs import Construct

class TimestreamStack(Stack):

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

        self.database_name = database_name
        self.table_name = table_name


