import json
import boto3
import urllib
from pprint import pprint

def search_celebrity(response, name):
    celebrityData = []
    for i in response['Items']:
        
        for item in i['celebrities']:
            if item['name'] == name:
               
                Dict = {
                    "filename": i['filename'],
                    "celebrity_name": item['name'],
                    "confidence": float(item['confidence']),
                    "Urls": item['Urls'],
                    "id": item['id']
                }
                
                celebrityData.append(Dict)
    
    celebrityData.sort(key=lambda i: i.get("filename"))
    return celebrityData
    
def search_celebrity_query(conf, response, name):
    celebrityData = []
    for i in response['Items']:
        found = False
        for item in i['celebrities']:
            confidence = float(item['confidence'])
            
            if item['name'] == name :
               
                if confidence>= float(conf):
                
                    Dict = {
                        "filename": i['filename'],
                        "celebrity_name":  item['name'],
                        "confidence": confidence,
                        "Urls": item['Urls'],
                        "id": item['id']
                    }
                    
                    celebrityData.append(Dict)
    
    celebrityData.sort(key=lambda i: i.get("filename"))
        
    return celebrityData
    
    
def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('celebrities')
    
    response = table.scan(
        ProjectionExpression="filename, celebrities"
    )
    
    name = event['pathParameters']['name']
    name = name.replace("%20", " ")
    
    if event['queryStringParameters'] is None:
        result = search_celebrity(response, name)
                    
        if not result:
            result = {
                "Error":"Celebrity not found"
            }
            return {
                'statusCode': 404,
                'body': json.dumps(result)
            }
            
            
        else:
            result = {
                "files" : result
            }
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
            
    elif 'queryStringParameters' in event and 'conf' in event['queryStringParameters']:
        result = search_celebrity_query(event['queryStringParameters']['conf'], response, name)
        
                    
        if not result:
            result = {
                "Error":"Celebrity not found"
            }
            return {
                'statusCode': 404,
                'body': json.dumps(result)
            }
            
            
        else:
            result = {
                "files" : result
            }
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
                    
                
    




