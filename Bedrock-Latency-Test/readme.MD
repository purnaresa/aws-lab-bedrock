# Bedrock Latency Test

**Performance benchmarking tool** for Amazon Bedrock AI models across different AWS regions.

## 🎯 **Use Case**

**Performance Optimization**: Measure and compare Bedrock model latency from different geographic locations to optimize user experience.

```
Client Init Time: 66.25 ms
Bedrock Processing Time: 875 ms
Bedrock Call Time: 907.82 ms
Estimated Network Latency: 32.82 ms
Total Runtime: 974.47 ms
```

## 📊 **Metrics Measured**

- ✅ **Client Init Time** - Boto3 client creation overhead
- ✅ **Bedrock Processing Time** - AI model inference time
- ✅ **Network Latency** - Round-trip network delay
- ✅ **Total Runtime** - End-to-end execution time

## 🌍 **Regional Performance Data**

| Application Region | Bedrock Region | Network Latency | Processing Time |
|-------------------|----------------|-----------------|----------------|
| N.Virginia | N.Virginia | 32 ms | 875 ms |
| Singapore | N.Virginia | 672 ms | 867 ms |
| Jakarta | N.Virginia | 731 ms | 856 ms |

## 📁 **Project Structure**

```
Bedrock-Latency-Test/
├── start.py      # Main benchmarking script with error handling
├── config.ini    # Configuration file
└── README.md     # This file
```

## 🚀 **Quick Start**

### **Prerequisites**

- Python 3.x
- AWS account with Bedrock access
- Configured AWS credentials

### **Step 1: Install Dependencies**

```bash
pip install boto3
```

### **Step 2: Configure Test Parameters**

Edit `config.ini` for your test scenario:

```ini
[DEFAULT]
region = us-east-1  # Test region
model_id = anthropic.claude-3-sonnet-20240229-v1:0
user_message = Describe the purpose of a 'hello world' program in one line.

[INFERENCE]
max_tokens = 512
temperature = 0.5
top_p = 0.9
```

### **Step 3: Run Benchmark**

```bash
python start.py
```

## 🔧 **Understanding the Output**

```
Client Init Time: 66.25 ms          # Boto3 client setup overhead
Input: Describe the purpose...        # Your test prompt
Response: The purpose of...           # AI model response
Bedrock Processing Time: 875 ms      # Pure AI inference time
Bedrock Call Time: 907.82 ms         # Total API call time
Estimated Network Latency: 32.82 ms  # Network round-trip delay
Total Runtime: 974.47 ms             # Complete execution time
```

### **Latency Breakdown**
```
Total Runtime
├── Client Init Time
├── Bedrock Call Time
│   ├── Network Latency (calculated)
│   └── Bedrock Processing Time (from API)
└── Other Processing Time
```

## 🛡️ **Reliability Features**

- ✅ **Retry logic** - Adaptive retry with exponential backoff
- ✅ **Error handling** - Specific error types and messages
- ✅ **Configuration validation** - Checks required sections
- ✅ **Connection pooling** - Optimized for multiple requests


## 📈 **Performance Analysis**

### **Key Insights from Testing**

1. **Processing Time Consistency**: ~875ms regardless of region
2. **Network Impact**: 20x latency increase for cross-region calls
3. **Client Overhead**: Minimal (~66ms) and consistent

### **Optimization Recommendations**

- **Same Region**: Deploy applications in same region as Bedrock
- **Model Selection**: Consider faster models for latency-sensitive apps
- **Caching**: Implement response caching for repeated queries
- **Async Processing**: Use async patterns for multiple requests


## 🚨 **Troubleshooting**

### **Common Issues**

**1. Model Access Denied**
```
AWS ClientError: AccessDeniedException
```
**Solution**: Enable model access in Bedrock console

**2. Invalid Model ID**
```
AWS ClientError: ValidationException
```
**Solution**: Check model availability in your region

**3. Configuration Error**
```
ERROR: Missing [INFERENCE] section in config.ini
```
**Solution**: Ensure all required config sections exist

## 💰 **Cost Considerations**

| Model | Input Cost | Output Cost | Use Case |
|-------|------------|-------------|----------|
| **Claude 3 Haiku** | $0.25/1M tokens | $1.25/1M tokens | Cost-effective testing |
| **Claude 3 Sonnet** | $3.00/1M tokens | $15.00/1M tokens | Balanced performance |
| **Claude 3 Opus** | $15.00/1M tokens | $75.00/1M tokens | Maximum quality |

## 🏷️ **Tags**

`aws` `bedrock` `performance` `latency` `benchmarking` `ai` `claude` `optimization`
