import json
import boto3
import os
from botocore.exceptions import ClientError, BotoCoreError
from botocore.config import Config

def lambda_handler(event, context):
    try:
        # Input validation
        if not event.get("body"):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing request body'})
            }
        
        # Parse JSON body
        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid JSON in request body'})
            }
        
        content = body.get("content", "").strip()
        if not content:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing or empty content field'})
            }
        
        # Validate content length
        if len(content) > 10000:  # 10KB limit
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Content too large (max 10KB)'})
            }

        # Create Bedrock client with retry configuration
        config = Config(
            retries={'max_attempts': 3, 'mode': 'adaptive'},
            max_pool_connections=10
        )
        
        region = os.environ.get('AWS_REGION', 'us-east-1')
        client = boto3.client("bedrock-runtime", region_name=region, config=config)

        # Get model ID from environment or use default
        model_id = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-haiku-20240307-v1:0')

        # Define the prompt for the model
        prompt = f"""Detect and mask only the sensitive personally identifiable information (PII) entities and their obfuscated versions in the following text: {content}. 
        
Replace each sensitive PII entity, such as names, email addresses, phone numbers (including obfuscated versions), and other personal identifiers, with asterisks (*) of the same length. 
        
However, do not mask any non-PII information, such as order numbers, product names, or other non-personal data. Keep all non-PII content unchanged. 
        
Do not include any additional text in the output."""

        # Format the request payload
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "temperature": 0,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        }

        # Invoke the model
        response = client.invoke_model(
            modelId=model_id, 
            body=json.dumps(native_request)
        )

        # Decode the response
        model_response = json.loads(response["body"].read())
        response_text = model_response["content"][0]["text"]

        return {
            'statusCode': 200,
            'body': json.dumps({
                'masked_content': response_text,
                'original_length': len(content),
                'processed_length': len(response_text)
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"AWS ClientError: {error_code} - {error_message}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'AWS service error',
                'details': f'{error_code}: {error_message}'
            })
        }
    
    except BotoCoreError as e:
        print(f"BotoCoreError: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'AWS connection error',
                'details': str(e)
            })
        }
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(e)
            })
        }
