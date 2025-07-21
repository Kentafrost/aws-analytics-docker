def handler(event, context):
    
    return {
        'isBase64Encoded':False,
        'statusCode': 200,
        'headers': {},
        'body': "Invoking Lambda Function with Docker image is successful."
    }