import json
import boto3
from urllib.parse import unquote_plus
from decimal import *

rekognition_client=boto3.client('rekognition')
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('celebrities')

def recognize_celebrities(bucket, key):
    response = rekognition_client.recognize_celebrities(
        Image={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    return response

def lambda_handler(event, context):
    
    record = event['Records'][0]
    event_name = record['eventName']
    key =unquote_plus(record['s3']['object']['key'], encoding='utf-8')
    bucket="polyu-comp3122a2-18086809d"
    
    if event_name == "ObjectCreated:Put":
        
        recog = recognize_celebrities(bucket, key)
        l =[]
        for celebrity in recog['CelebrityFaces']:
            Dict = {
                "confidence": Decimal(celebrity['MatchConfidence']),
                "id": celebrity['Id'],
                "name": celebrity['Name'],
                "Urls": celebrity['Urls']
            } 
            
            l.append(Dict)
        

        table.put_item(
            Item = {
                "filename" : key,
                "celebrities" : l
            }
        )

    if event_name == "ObjectRemoved:Delete":
        table.delete_item(
            Key={
                "filename" : key
            }
        )

