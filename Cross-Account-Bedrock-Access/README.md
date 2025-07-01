# Cross-Account Bedrock Access

This project demonstrates **secure cross-account access to Amazon Bedrock** using AWS Security Token Service (STS) role assumption with security best practices.

## 🎯 **Use Case**

**Enterprise Scenario**: A central AWS account manages Bedrock access and billing, while multiple client accounts need to use AI models without direct Bedrock permissions.

```
┌─────────────────┐    Assume Role    ┌─────────────────┐
│  Client Account │ ─────────────────▶│ Bedrock Account │
│  (123456789995) │                   │  (123456787214) │
│                 │◀──────────────────│                 │
└─────────────────┘  Temp Credentials └─────────────────┘
```

## 🔒 **Security Features**

- ✅ **External ID** - Prevents confused deputy attacks
- ✅ **Temporary credentials** - Auto-expire in 1 hour
- ✅ **Least privilege** - Only invoke specific models
- ✅ **Audit trail** - All actions logged in CloudTrail
- ✅ **No long-term secrets** - No hardcoded credentials

## 📁 **Project Structure**

```
Cross-Account-Bedrock-Access/
├── starter.py              # Main application with detailed comments
├── config.ini              # Configuration file
├── permission/
│   ├── CrossAccountRole.yaml    # Role in Bedrock account
│   └── ClientAccessRole.yaml    # Role in client account
└── README.md               # This file
```

## 🚀 **Quick Start**

### **Step 1: Deploy Infrastructure**

**In Bedrock Account (123456787214):**
```bash
aws cloudformation create-stack \
  --stack-name BedrockCrossAccountRole \
  --template-body file://permission/CrossAccountRole.yaml \
  --parameters ParameterKey=ClientAccountId,ParameterValue=123456789995 \
  --capabilities CAPABILITY_NAMED_IAM
```

**In Client Account (123456789995):**
```bash
aws cloudformation create-stack \
  --stack-name ClientAccessRole \
  --template-body file://permission/ClientAccessRole.yaml \
  --parameters ParameterKey=BedrockAccountId,ParameterValue=123456787214 \
  --capabilities CAPABILITY_NAMED_IAM
```

### **Step 2: Configure Application**

Update `config.ini` with your account IDs:
```ini
[AWS]
RoleArn = arn:aws:iam::YOUR_BEDROCK_ACCOUNT:role/BedrockCrossAccountAccessRole
ExternalId = YOUR_CLIENT_ACCOUNT_ID
SessionDuration = 3600

[Bedrock]
ModelId = anthropic.claude-3-sonnet-20240229-v1:0
```

### **Step 3: Install Dependencies**

```bash
pip install boto3 llama-index-llms-bedrock
```

### **Step 4: Run Application**

```bash
python starter.py
```

## 🔧 **How It Works**

### **1. Role Assumption Process**
```python
# Client assumes role in Bedrock account
assumed_role_object = sts_client.assume_role(
    RoleArn=role_arn,
    RoleSessionName="AssumeRoleSession1",
    ExternalId=external_id,        # Security: Prevents confused deputy
    DurationSeconds=session_duration  # Limits credential lifetime
)
```

### **2. Temporary Credentials**
```python
# Extract temporary credentials (valid for 1 hour max)
credentials = assumed_role_object['Credentials']
# - AccessKeyId: Temporary access key
# - SecretAccessKey: Temporary secret key
# - SessionToken: Required for temporary credentials
# - Expiration: When credentials expire
```

### **3. Secure Bedrock Access**
```python
# Create Bedrock client with temporary credentials
bedrock_client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)
```

## 🛡️ **Security Best Practices Implemented**

### **External ID Protection**
```yaml
# In CrossAccountRole.yaml
Condition:
  StringEquals:
    'sts:ExternalId': !Ref ClientAccountId  # Prevents confused deputy attacks
```

### **Specific Principal (Not Account Root)**
```yaml
# Secure: Specific role can assume
Principal:
  AWS: !Sub 'arn:aws:iam::${ClientAccountId}:role/AssumeBedrockRole'

# Insecure: Entire account can assume
# Principal:
#   AWS: !Sub 'arn:aws:iam::${ClientAccountId}:root'
```

### **Limited Permissions**
```yaml
# Only specific Bedrock actions allowed
Action:
  - 'bedrock:InvokeModel'
  - 'bedrock:InvokeModelWithResponseStream'
Resource: 
  - 'arn:aws:bedrock:*::foundation-model/anthropic.claude*'
  - 'arn:aws:bedrock:*::foundation-model/amazon.titan*'
```

### **Time-Based Conditions**
```yaml
# Role only works after specific date
Condition:
  DateGreaterThan:
    'aws:CurrentTime': '2024-01-01T00:00:00Z'
```

## 📊 **Cost Considerations**

| Component | Cost | Notes |
|-----------|------|-------|
| **STS API Calls** | Free | First 1M calls/month |
| **Bedrock Usage** | Pay-per-use | Based on model and tokens |
| **CloudTrail Logging** | ~$2/month | For audit trail |

## 🔍 **Monitoring & Auditing**

### **CloudTrail Events to Monitor**
- `AssumeRole` - When cross-account access occurs
- `InvokeModel` - When Bedrock models are called
- `GetSessionToken` - STS token requests

### **CloudWatch Metrics**
- Role assumption frequency
- Session duration patterns
- Failed authentication attempts

## 🚨 **Troubleshooting**

### **Common Issues**

**1. Access Denied Error**
```
ClientError: An error occurred (AccessDenied) when calling the AssumeRole operation
```
**Solution**: Check External ID matches client account ID

**2. Invalid Role ARN**
```
ClientError: An error occurred (InvalidUserID.NotFound)
```
**Solution**: Verify role exists in target account

**3. Session Duration Error**
```
ClientError: An error occurred (ValidationError) when calling the AssumeRole operation
```
**Solution**: Ensure DurationSeconds ≤ MaxSessionDuration (3600)

### **Debug Steps**
1. Verify both CloudFormation stacks deployed successfully
2. Check IAM role trust relationships
3. Confirm External ID matches in both config and role
4. Test with AWS CLI: `aws sts assume-role --role-arn <ARN> --role-session-name test --external-id <ID>`

## 📚 **Additional Resources**

- [AWS STS AssumeRole Documentation](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)
- [Cross-Account Access Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html)
- [Confused Deputy Problem](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/)

## 🏷️ **Tags**

`aws` `bedrock` `cross-account` `security` `sts` `iam` `ai` `llm` `enterprise`
