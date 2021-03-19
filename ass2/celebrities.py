import json
import boto3
import urllib

def celebrity_data(response, result):
    
    for i in response['Items']:
            for item in i['celebrities']:
                        
                
                Dict = {
                    "filename": i['filename'],
                    "confidence":  float(item['confidence']),
                    "Urls": item['Urls'],
                    "id": item['id']
                }
                
                if item['name'] not in result.keys():
                    celebrity = []
                    celebrity.append(Dict)
                    result[item['name']] = celebrity
                    
                elif item['name'] in result.keys():
                    celebrity = []
                    
                    celebrity = result[item['name']]
                    celebrity.append(Dict)
                    celebrity.sort(key=lambda i: i.get("filename"))
                    result[item['name']] = celebrity
    return result

def celebrity_data_query(compare_conf, response, result):
    
    
    for i in response['Items']:
            for item in i['celebrities']:
                confidence = float(item['confidence'])
                
                if confidence >= float(compare_conf):
                    
                    Dict = {
                        "filename": i['filename'],
                        "confidence": confidence,
                        "Urls": item['Urls'],
                        "id": item['id']
                    }
                
                    if item['name'] not in result.keys():
                        celebrity = []
                        celebrity.append(Dict)
                        result[item['name']] = celebrity
                        
                    elif item['name'] in result.keys():
                        celebrity = []
                        celebrity = result[item['name']]
                        celebrity.append(Dict)
                        celebrity.sort(key=lambda i: i.get("filename"))
                        result[item['name']] = celebrity
    return result

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('celebrities')
    
    response = table.scan(
        ProjectionExpression="filename, celebrities"
    )
    
    result = {}
    
    if event['queryStringParameters'] is None:
        result = celebrity_data(response, result)
    
    elif 'queryStringParameters' in event and 'conf' in event['queryStringParameters']:
        result = celebrity_data_query(event['queryStringParameters']['conf'], response, result)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }