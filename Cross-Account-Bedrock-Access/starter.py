import boto3
from llama_index.llms.bedrock import Bedrock
import configparser

# Cross-Account Bedrock Access with External ID Security
# Demonstrates secure role assumption to prevent confused deputy attacks

# Read configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Get configuration values
role_arn = config['AWS']['RoleArn']  # Target role in Bedrock account
external_id = config['AWS']['ExternalId']  # Security: prevents confused deputy attacks
session_duration = config.getint('AWS', 'SessionDuration')  # Max 1 hour
model_id = config['Bedrock']['ModelId']

# Step 1: Assume cross-account role with security controls
sts_client = boto3.client('sts')
assumed_role_object = sts_client.assume_role(
    RoleArn=role_arn,
    RoleSessionName="AssumeRoleSession1",  # For CloudTrail auditing
    ExternalId=external_id,  # CRITICAL: Prevents confused deputy attacks
    DurationSeconds=session_duration  # Limits credential lifetime
)

# Step 2: Extract temporary credentials
credentials = assumed_role_object['Credentials']
# Contains: AccessKeyId, SecretAccessKey, SessionToken, Expiration

# Step 3: Create Bedrock client with temporary credentials
bedrock_client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken'],  # Required for temp credentials
    region_name='us-east-1'
)

# Step 4: Initialize LlamaIndex Bedrock LLM
llm = Bedrock(client=bedrock_client, model=model_id)

# Step 5: Generate AI response using cross-account credentials
response = llm.complete("Tell me about Indonesia.")
print(response)

# Security: External ID + temp credentials + least privilege + audit trail
