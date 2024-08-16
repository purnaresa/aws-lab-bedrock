from llama_index.llms.bedrock_converse import BedrockConverse

# Create an instance of the BedrockConverse LLM
# This will be used to interact with the Amazon Bedrock model in a conversational manner
llm = BedrockConverse(
    model="meta.llama3-70b-instruct-v1:0",
    profile_name="default",
)

# Call the complete method to generate a response from the model
# The model will complete the provided prompt
resp = llm.complete("tell me the coffee origin")

# Print the response from the model
print(resp)
