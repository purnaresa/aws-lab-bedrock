# AWS Lab Bedrock

**Production-ready examples** showcasing Amazon Bedrock integration patterns with security best practices.

## 🎯 **Overview**

This repository demonstrates **three key use cases** for Amazon Bedrock in enterprise environments, each following AWS Well-Architected principles.

```
aws-lab-bedrock/
├── Cross-Account-Bedrock-Access/    # Enterprise security pattern
├── PII-Scanner/                     # Data privacy compliance
├── Bedrock-Latency-Test/           # Performance optimization
└── README.md                       # This file
```

## 🏗️ **Use Cases**

### **1. Cross-Account Bedrock Access** 🔒
**Enterprise Security Pattern**

Secure cross-account access to Bedrock using STS role assumption with External ID protection.

- ✅ **External ID** prevents confused deputy attacks
- ✅ **Temporary credentials** with 1-hour expiration
- ✅ **Least privilege** IAM policies
- ✅ **Audit trail** through CloudTrail

**When to use**: Multi-account organizations with centralized AI governance

[📖 View Documentation](./Cross-Account-Bedrock-Access/README.md)

---

### **2. PII Scanner** 🛡️
**Data Privacy Compliance**

AI-powered detection and masking of Personally Identifiable Information in Indonesian text.

- ✅ **Serverless** Lambda + API Gateway architecture
- ✅ **Cost-optimized** using Claude 3 Haiku
- ✅ **Production-ready** error handling and validation
- ✅ **Compliance-focused** for data privacy regulations

**When to use**: Applications processing sensitive customer data

[📖 View Documentation](./PII-Scanner/README.md)

---

### **3. Bedrock Latency Test** 📊
**Performance Optimization**

Benchmarking tool to measure Bedrock model performance across regions.

- ✅ **Multi-region** latency comparison
- ✅ **Detailed metrics** breakdown
- ✅ **Retry logic** for reliability
- ✅ **Cost analysis** for different models

**When to use**: Optimizing user experience and cost efficiency

[📖 View Documentation](./Bedrock-Latency-Test/readme.MD)

## 🚀 **Quick Start**

### **Prerequisites**
- AWS account with Bedrock access
- Python 3.x
- AWS CLI configured
- Required permissions for each use case

### **Choose Your Use Case**

```bash
# Enterprise Security
cd Cross-Account-Bedrock-Access/
python starter.py

# Data Privacy
cd PII-Scanner/
sam deploy --guided

# Performance Testing
cd Bedrock-Latency-Test/
python start.py
```

## 🏛️ **Architecture Patterns**

### **Cross-Account Access**
```
┌─────────────────┐    Assume Role    ┌─────────────────┐
│  Client Account │ ──────────────────▶│ Bedrock Account │
│                 │◀──────────────────│                 │
└─────────────────┘   Temp Credentials └─────────────────┘
```

### **PII Scanner**
```
API Gateway → Lambda → Bedrock (Claude 3 Haiku) → Masked Response
```

### **Latency Test**
```
Client → Bedrock API → Metrics Collection → Performance Analysis
```

## 💰 **Cost Optimization**

| Use Case | Primary Cost | Optimization Strategy |
|----------|--------------|----------------------|
| **Cross-Account** | Bedrock usage | Centralized billing, shared resources |
| **PII Scanner** | Lambda + Bedrock | Claude 3 Haiku ($0.25/1M tokens) |
| **Latency Test** | Bedrock calls | Minimal test prompts, efficient models |

## 🛡️ **Security Best Practices**

### **Implemented Across All Projects**
- ✅ **Least privilege** IAM policies
- ✅ **Input validation** and sanitization
- ✅ **Error handling** without information leakage
- ✅ **Audit logging** for compliance
- ✅ **No hardcoded credentials**

### **Project-Specific Security**
- **Cross-Account**: External ID, temporary credentials
- **PII Scanner**: Content size limits, structured error responses
- **Latency Test**: Retry logic, configuration validation

## 📊 **Performance Benchmarks**

### **Regional Latency (to us-east-1)**
| Region | Network Latency | Total Time |
|--------|----------------|------------|
| us-east-1 | 32 ms | 974 ms |
| ap-southeast-1 | 672 ms | 1539 ms |
| ap-southeast-3 | 731 ms | 1587 ms |

### **Model Performance**
| Model | Speed | Cost | Use Case |
|-------|-------|------|----------|
| Claude 3 Haiku | Fast | Low | PII scanning, testing |
| Claude 3 Sonnet | Medium | Medium | General purpose |
| Claude 3 Opus | Slow | High | Complex reasoning |

## 🔍 **Monitoring & Observability**

### **CloudWatch Metrics**
- Bedrock model invocations
- Lambda execution metrics
- API Gateway request counts
- Error rates and latencies

### **CloudTrail Events**
- Cross-account role assumptions
- Bedrock API calls
- Lambda function invocations

## 🚨 **Common Issues & Solutions**

### **Bedrock Access**
```
AccessDeniedException: User is not authorized to perform: bedrock:InvokeModel
```
**Solution**: Enable model access in Bedrock console → Model access

### **Cross-Account Setup**
```
AccessDenied when calling AssumeRole operation
```
**Solution**: Verify External ID matches client account ID

### **Lambda Timeout**
```
Task timed out after 30.00 seconds
```
**Solution**: Increase timeout or optimize prompt size

## 📚 **Additional Resources**

- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Cross-Account Access Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Follow security best practices
4. Add comprehensive tests
5. Update documentation
6. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏷️ **Tags**

`aws` `bedrock` `ai` `security` `enterprise` `serverless` `cross-account` `pii` `performance` `well-architected`

---

**Built with ❤️ for the AWS community**