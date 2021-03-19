import json
import boto3
import urllib
from pprint import pprint

def list_celebrities(table):
    response = table.scan(
        ProjectionExpression="celebrities"
    )
    celebrities= []
    for i in response['Items']:
        for item in i['celebrities']:
            if item['name'] not in celebrities:
                celebrities.append(item['name'])
    
    
    result = {
        "celebrities_names":celebrities
    }
    return result
    

def lambda_handler(event, context):
    
    
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('celebrities')
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(list_celebrities(table))
    }
