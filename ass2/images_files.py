import json
import boto3
import urllib
from pprint import pprint

def image_details(filename, response):
    image_details = []
    for i in response['Items']:
        file = {}
        if filename == i['filename']:
            
            list = []
            for item in i['celebrities']:
            
                Dict = {
                    "name": item['name'],
                    "confidence": float(item['confidence']),
                    
                    "Urls": item['Urls'],
                    "id": item['id']
                }
                image_details.append(Dict)
            image_details.sort(key=lambda i: i.get("name"))
            
            file = {
                "celebrities": image_details,
                "filename": i['filename']
            }
            
            image_details =[]
    return file


def image_details_query(filename, confidence, response ):
    
    found = False
    image_details = []
    for i in response['Items']:
        if filename == i['filename']:
            file = {}
            list = []
            for item in i['celebrities']:
                
                if float(item['confidence']) >= confidence:
            
                    Dict = {
                        "name": item['name'],
                        "confidence": float(item['confidence']),
                        "Urls": item['Urls'],
                        "id": item['id']
                    }
                    image_details.append(Dict)
                    
            image_details.sort(key=lambda i: i.get("name"))
            
            file = {
                "celebrities": image_details,
                "filename": i['filename']
            }
            
            image_details =[]
            
    return file

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('celebrities')
    
    response = table.scan(
        ProjectionExpression="filename, celebrities"
    )
    
    result = {}
    
    filename = event['pathParameters']['filename']
    filename = filename.replace("%20", " ")
    
    if event['queryStringParameters'] is None:
        result = image_details(filename, response)
        
        if not result:
            result = {
                "Error":"Image not found"
            }
            return {
                'statusCode': 404,
                'body': json.dumps(result)
            }
            
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
            
    elif 'conf' in event['queryStringParameters']:
        
        result = image_details_query(filename, float(event['queryStringParameters']['conf']), response)
        
                    
        if not result:
            result = {
                "Error":"Image not found"
            }
            return {
                'statusCode': 404,
                'body': json.dumps(result)
            }
            
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
                
    




