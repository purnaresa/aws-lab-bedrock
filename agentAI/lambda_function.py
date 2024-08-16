import json
import boto3

# Create a Bedrock Agent Runtime client
bedrock_runtime_client = boto3.client('bedrock-agent-runtime')

def lambda_handler(event, context):
    # Print the entire event object
    print("Received event:", json.dumps(event, indent=2))

    # Get the content from the request body
    body = event.get("body", "")
    if body:
        content = json.loads(body).get("content", "")
    else:
        content = ""

    # Invoke the Bedrock agent with the user input
    response = bedrock_runtime_client.invoke_agent(
        agentId='KDW5T0NGQA',
        agentAliasId='HIFHTZZ9S3',
        sessionId='1',
        inputText=content
    )

    # Process the response from the agent
    agent_response = ''
    for event in response['completion']:
        agent_response += event['chunk']['bytes'].decode()

    # Return the agent's response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': agent_response
        })
    }
