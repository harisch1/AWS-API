import json

def lambda_handler(event, context):
    # TODO implement
    
    result = {
        "id": "18086809D",
        "name": "Choudhary Muhammad Haris"
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
