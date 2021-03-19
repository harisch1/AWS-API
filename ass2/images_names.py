import json
import boto3
import urllib
import pprint
pp = pprint.PrettyPrinter(indent=4)
s3 = boto3.client('s3')
def list_objects(bucket_name): 
    response = s3.list_objects(Bucket=bucket_name)
    images = []
    for item in response['Contents']:
        images.append(item['Key'])
    #return images
    print(images)
    result = {
        "images": images
    }
    return result
    #pp.pprint (str(response['Contents']))
    
    
def lambda_handler(event, context):
    bucket_name = 'polyu-comp3122a2-18086809d'
    result = list_objects(bucket_name) #list objects in bucket
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }