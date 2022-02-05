def handler(event, context):
    print("\U0001F4C2 Starting function after trigger")
    print(event)     
    return {
        'statusCode': 200,
        'body': 'File is uploaded',
    }

