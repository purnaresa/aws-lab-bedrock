import json
import boto3

from botocore.exceptions import ClientError

def lambda_handler(event, context):
        # Print the entire event object
    print("Received event:", json.dumps(event, indent=2))

    # Get the content from the request body
    body = event.get("body", "")
    if body:
        content = json.loads(body).get("content", "")
    else:
        content = ""

    # Create a Bedrock Runtime client in the AWS Region of your choice.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Claude 3 Haiku.
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    # Define the prompt for the model.
    
    prompt = f"Detect and mask only the sensitive personally identifiable information (PII) entities and their obfuscated versions in the following text: {content}. Replace each sensitive PII entity, such as names (e.g., J0hn D0e), email addresses (e.g., j0hn.d0e@example.com), phone numbers (including obfuscated versions with special characters or spacing, e.g., o821-1488-68o7), and other personal identifiers, with asterisks (*) of the same length. However, do not mask any non-PII information, such as order numbers (e.g., #12345), product names (e.g., Widget X), or other non-personal data. Keep all non-PII content unchanged. Replace the name part of each email address with asterisks (*) of the same length, while keeping the domain and non-PII content unchanged. Do not include any additional text in the output."

    # Format the request payload using the model's native structure.
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

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=model_id, body=request)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    response_text = model_response["content"][0]["text"]

    return {
        'statusCode': 200,
        'body': response_text
    }
