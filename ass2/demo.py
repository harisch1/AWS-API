import json

def lambda_handler(event, context):
    # TODO implement
    
    result = {"about":"comp3122 assignment 2"}
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
