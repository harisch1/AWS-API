import json
import boto3
import urllib
from pprint import pprint

def images(response):
    result = []
    celebrityData = []
    
    for i in response['Items']:
        files = {}
        for item in i['celebrities']:
           
            Dict = {
                "confidence": float(item['confidence']),
                "name": item['name'],
                "Urls": item['Urls'],
                "id": item['id']
            }
            celebrityData.append(Dict)
        celebrityData.sort(key=lambda i: i.get("name"))
        
        files = {
            "filename": i['filename'],
            "celebrities": celebrityData
        }
        
        result.append(files)
        celebrityData =[]
    result.sort(key=lambda i: i.get("filename"))
    return result    


def images_query(conf, response):
    
    result = []
    celebrityData = []
    
    for i in response['Items']:
        files = {}
        for item in i['celebrities']:
            if float(item['confidence']) >= float(conf):
                Dict = {
                    "confidence": float(item['confidence']),
                    "name": item['name'],
                    "Urls": item['Urls'],
                    "id": item['id']
                }
                celebrityData.append(Dict)
                
        celebrityData.sort(key=lambda i: i.get("name"))
        files = {
            "filename": i['filename'],
            "celebrities": celebrityData
        }
        
        result.append(files)
        celebrityData =[]
    result.sort(key=lambda i: i.get("filename"))
    
    return result    
        

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('celebrities')
    
    response = table.scan(
        ProjectionExpression="filename, celebrities"
    )
    
    if event['queryStringParameters'] is None:
        result = images(response)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    
    elif 'conf' in event['queryStringParameters']:
        conf = event['queryStringParameters']['conf']
        result = images_query(conf, response)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }