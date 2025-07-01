import boto3
from botocore.exceptions import ClientError, BotoCoreError
from botocore.config import Config
import time
import configparser
import sys

def main():
    # Start timing the entire process
    start_time = time.time()

    try:
        # Read configuration
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Validate configuration
        required_sections = ['DEFAULT', 'INFERENCE']
        for section in required_sections:
            if not config.has_section(section):
                print(f"ERROR: Missing [{section}] section in config.ini")
                sys.exit(1)

        # Create Bedrock client with retry configuration
        boto_config = Config(
            retries={'max_attempts': 3, 'mode': 'adaptive'},
            max_pool_connections=10
        )
        
        start_time_client = time.time()
        client = boto3.client(
            "bedrock-runtime", 
            region_name=config['DEFAULT']['region'],
            config=boto_config
        )
        end_time_client = time.time()
        client_init_time = (end_time_client - start_time_client) * 1000
        print(f"Client Init Time: {client_init_time:.2f} ms\n")

        # Get configuration values
        model_id = config['DEFAULT']['model_id']
        user_message = config['DEFAULT']['user_message']
        
        conversation = [
            {
                "role": "user",
                "content": [{"text": user_message}],
            }
        ]
        print("Input:", user_message)

        # Make Bedrock API call with timing
        bedrock_call_start = time.time()
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": config.getint('INFERENCE', 'max_tokens'),
                "temperature": config.getfloat('INFERENCE', 'temperature'),
                "topP": config.getfloat('INFERENCE', 'top_p')
            },
        )
        bedrock_call_end = time.time()
        
        # Extract and display results
        response_text = response["output"]["message"]["content"][0]["text"]
        latency = response["metrics"]["latencyMs"]
        bedrock_call_time = (bedrock_call_end - bedrock_call_start) * 1000
        
        print(f"Response: {response_text} \n")
        print(f"Bedrock Processing Time: {latency} ms")
        print(f"Bedrock Call Time: {bedrock_call_time:.2f} ms")
        
        # Calculate network latency estimate
        network_latency = bedrock_call_time - latency
        print(f"Estimated Network Latency: {network_latency:.2f} ms")

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"AWS ClientError: {error_code} - {error_message}")
        sys.exit(1)
    
    except BotoCoreError as e:
        print(f"BotoCoreError: {str(e)}")
        sys.exit(1)
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)
    
    finally:
        # Calculate and print the total runtime
        end_time = time.time()
        total_runtime = (end_time - start_time) * 1000
        print(f"Total Runtime: {total_runtime:.2f} ms\n")

if __name__ == "__main__":
    main()
