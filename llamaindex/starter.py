from llama_index.llms.bedrock import Bedrock

# Create an instance of the Bedrock LLM
# This will be used to interact with the Amazon Bedrock model
llm = Bedrock(model="anthropic.claude-3-5-sonnet-20240620-v1:0", profile_name="default")

# Call the complete method to generate a response from the model
# The model will complete the provided prompt
resp = llm.complete("Tell me about Indonesia ")

# Print the response from the model
print(resp)
