import os
import boto3
import uuid
import time

DATABASE_NAME = os.environ['DATABASE_NAME']
TABLE_NAME = os.environ['TABLE_NAME']

client = boto3.client('timestream-write')

def on_event(event, context):
  print(event)
  request_type = event['RequestType']
  if request_type == 'Create': return on_create(event)
  if request_type == 'Update': return on_update(event)
  if request_type == 'Delete': return on_delete(event)
  raise Exception("Invalid request type: %s" % request_type)

def on_create(event):
  props = event["ResourceProperties"]
  print("Create new resource with props %s" % props)

  _record_event(event)

  physical_id = str(uuid.uuid4())

  return { 'PhysicalResourceId': physical_id }

def on_update(event):
  physical_id = event["PhysicalResourceId"]
  props = event["ResourceProperties"]

  _record_event(event)
  
  print("Update resource %s with props %s" % (physical_id, props))

def on_delete(event):
  physical_id = event["PhysicalResourceId"]
  props = event["ResourceProperties"]

  _record_event(event)

  print("Delete resource %s with props %s" % (physical_id, props))

def _record_event(event):
  request_type = event['RequestType']
  props = event["ResourceProperties"]

  approach = props["Approach"]
  resource_version = props["ResourceVersion"]
  resource_name = props["ResourceName"]

  epoch_time_ms = int(time.time() * 1000)

  client.write_records(
    DatabaseName=DATABASE_NAME,
    TableName=TABLE_NAME,
    Records=[
      {
        'Dimensions': [
          {
            'Name': 'operation',
            'Value': request_type.lower(),
            'DimensionValueType': 'VARCHAR'
          },
          {
            'Name': 'approach',
            'Value': approach,
            'DimensionValueType': 'VARCHAR'
          },
          {
            'Name': 'resource',
            'Value': resource_name,
            'DimensionValueType': 'VARCHAR'
          },
          {
            'Name': 'version',
            'Value': resource_version,
            'DimensionValueType': 'VARCHAR'
          },
        ],
        'Time': str(epoch_time_ms),
        'TimeUnit': 'MILLISECONDS',
        'MeasureName': 'dummy',
        'MeasureValue': 'dummy',
        'MeasureValueType': 'VARCHAR'
      }
    ]
  )

