# PII Scanner

AI-powered **Personally Identifiable Information (PII) detection and masking** using Amazon Bedrock and AWS Lambda.

## 🎯 **Use Case**

**Data Privacy Compliance**: Automatically detect and mask sensitive information in Indonesian text before processing or storage.

```
Input:  "Nama saya Resa. Email saya purnaresa@gmail.com"
Output: "Nama saya ****. Email saya **********@gmail.com"
```

## 🔒 **PII Types Detected**

- ✅ **Names** - Indonesian names
- ✅ **Email addresses** - Masks username, keeps domain
- ✅ **Phone numbers** - Including obfuscated formats (o821-1488-68o7)
- ✅ **ID numbers** - KTP, NPWP, employee IDs
- ✅ **Addresses** - Street addresses
- ❌ **Non-PII preserved** - Order numbers, product names

## 📁 **Project Structure**

```
PII-Scanner/
├── lambda_function.py    # Main Lambda function with error handling
├── template.yaml         # SAM template with security policies
├── event*.json          # Test events for different PII types
└── README.md            # This file
```

## 🚀 **Quick Start**

### **Step 1: Deploy with SAM**

```bash
# Install SAM CLI first
pip install aws-sam-cli

# Deploy the function
sam build
sam deploy --guided
```

### **Step 2: Test Locally**

```bash
# Test with different PII types
sam local invoke ScanPIIFunction -e event.json
sam local invoke ScanPIIFunction -e event-ktp.json
sam local invoke ScanPIIFunction -e event-address.json
```

### **Step 3: Test via API**

```bash
# Get API endpoint from SAM output
curl -X POST https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/Prod/scan \
  -H "Content-Type: application/json" \
  -d '{"content": "Nama saya Resa. Email saya purnaresa@gmail.com"}'
```

## 🔧 **How It Works**

### **1. Input Validation**
```python
# Validates JSON structure, content presence, and size limits
if len(content) > 10000:  # 10KB limit
    return {'statusCode': 400, 'body': 'Content too large'}
```

### **2. AI-Powered Detection**
```python
# Uses Claude 3 Haiku for cost-effective PII detection
model_id = 'anthropic.claude-3-haiku-20240307-v1:0'
prompt = "Detect and mask PII entities with asterisks..."
```

### **3. Structured Response**
```json
{
  "masked_content": "Nama saya ****. Email saya **********@gmail.com",
  "original_length": 45,
  "processed_length": 42
}
```

## 📊 **Test Cases Included**

| File | PII Types | Example |
|------|-----------|---------|
| `event.json` | Name, email, phone | Basic PII detection |
| `event-ktp.json` | KTP, NPWP numbers | Indonesian ID numbers |
| `event-address.json` | Name, address | Location information |
| `event-internal.json` | Employee ID, phone | Internal company data |

## 🛡️ **Security Features**

- ✅ **Input validation** - Size limits and format checks
- ✅ **Error handling** - Proper HTTP status codes
- ✅ **Least privilege IAM** - Only Bedrock invoke permissions
- ✅ **Environment variables** - Configurable model selection
- ✅ **Retry logic** - Resilient to transient failures

## 💰 **Cost Optimization**

| Component | Cost | Optimization |
|-----------|------|--------------|
| **Claude 3 Haiku** | $0.25/1M input tokens | Cheapest Claude model |
| **Lambda** | $0.20/1M requests | Serverless, pay-per-use |
| **API Gateway** | $3.50/1M requests | RESTful API access |

**Estimated cost**: ~$0.01 per 1000 PII scans

## 🔍 **Monitoring**

### **CloudWatch Metrics**
- Lambda invocations and errors
- API Gateway request count
- Bedrock model invocation metrics

### **CloudWatch Logs**
- Request/response logging
- Error details and stack traces
- Performance metrics

## 🚨 **Troubleshooting**

### **Common Issues**

**1. Model Access Denied**
```json
{"error": "AWS service error", "details": "AccessDeniedException"}
```
**Solution**: Enable Bedrock model access in AWS Console

**2. Invalid JSON**
```json
{"error": "Invalid JSON in request body"}
```
**Solution**: Ensure proper JSON format with "content" field

**3. Content Too Large**
```json
{"error": "Content too large (max 10KB)"}
```
**Solution**: Split large content into smaller chunks

## 📚 **Configuration**

### **Environment Variables**
- `BEDROCK_MODEL_ID` - Model to use (default: Claude 3 Haiku)
- `AWS_REGION` - AWS region (default: us-east-1)

### **SAM Parameters**
- `BedrockModelId` - Override default model during deployment

## 🏷️ **Tags**

`aws` `bedrock` `lambda` `pii` `privacy` `compliance` `ai` `serverless` `sam`