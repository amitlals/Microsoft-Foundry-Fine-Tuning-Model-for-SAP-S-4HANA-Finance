# Examples

This directory contains example scripts and utilities for working with the SAP Finance fine-tuned model.

## Files

### `test_model.py`

Interactive testing script for the deployed fine-tuned model.

**Features**:
- Automated test suite with 13 predefined SAP Finance queries
- Interactive mode for custom queries
- Single query testing
- Response time and token usage tracking

**Setup**:
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export DEPLOYMENT_NAME="sap-finance-gpt4o-mini"

# Run the script
python test_model.py
```

**Usage Options**:
1. **Automated Test Suite**: Run 13 predefined queries automatically
2. **Interactive Mode**: Ask custom questions in real-time
3. **Single Query Test**: Test one specific query with detailed output

### `validate_dataset.py`

Validation utility for training and validation datasets.

**Features**:
- JSONL format validation
- Message structure verification
- Token count estimation
- Cost estimation
- Detailed error reporting

**Usage**:
```bash
python validate_dataset.py
```

**Validates**:
- Correct JSONL format
- Required fields (role, content)
- Valid roles (system, user, assistant)
- Proper conversation structure
- Non-empty content

**Output**:
- ✅ Valid/❌ Invalid status per file
- Statistics (lines, messages, tokens)
- Role distribution
- Estimated fine-tuning cost
- Detailed error messages if issues found

### `requirements.txt`

Python package dependencies for the example scripts.

**Packages**:
- `openai>=1.0.0` - Azure OpenAI SDK
- `requests>=2.31.0` - HTTP library (optional)
- `python-dotenv>=1.0.0` - Environment variable management (optional)
- `jsonschema>=4.19.0` - JSON validation (optional)

**Installation**:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Validate Your Datasets

Before fine-tuning, ensure your datasets are valid:

```bash
cd examples
python validate_dataset.py
```

Expected output:
```
✅ All datasets are VALID and ready for Azure OpenAI fine-tuning!
Training examples: 13
Validation examples: 4
```

### 2. Deploy Fine-Tuned Model

Follow the [Setup Guide](../docs/SETUP_GUIDE.md) to:
1. Upload datasets to Azure AI Foundry
2. Configure and start fine-tuning
3. Deploy the fine-tuned model
4. Get deployment credentials

### 3. Test the Model

After deployment, test your model:

```bash
# Set your credentials
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export DEPLOYMENT_NAME="sap-finance-gpt4o-mini"

# Run tests
python test_model.py
```

Choose from the menu:
- Option 1: Run full test suite
- Option 2: Interactive Q&A mode
- Option 3: Single query test

## Example Interactions

### Transaction Code Query
```
You: What is transaction code FB50?

🤖 Assistant: FB50 is the SAP transaction code used to post G/L account 
documents directly in Financial Accounting (FI). It allows you to:
1. Create manual journal entries directly to General Ledger accounts
2. Post complex entries with multiple line items
3. Handle corrections and adjustments
...
```

### Configuration Question
```
You: How do I configure automatic account determination for inventory?

🤖 Assistant: Automatic account determination for inventory (Material 
Management) ensures that goods movements automatically post to the 
correct G/L accounts. This is configured in transaction OBYC...
```

### Process Guidance
```
You: How do I run month-end closing in SAP?

🤖 Assistant: Month-end closing in SAP is a comprehensive process 
involving both Financial Accounting (FI) and Controlling (CO) modules.
Here's a structured approach:

Pre-Closing Activities:
1. Verify Open Periods (Transaction: OB52)
...
```

## Integration Examples

### Basic Python Integration

```python
from openai import AzureOpenAI
import os

# Initialize client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Ask a question
response = client.chat.completions.create(
    model="sap-finance-gpt4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are an SAP S/4HANA Finance expert."
        },
        {
            "role": "user",
            "content": "What is the difference between FB50 and F-02?"
        }
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### REST API Example

```bash
curl https://your-resource.openai.azure.com/openai/deployments/sap-finance-gpt4o-mini/chat/completions?api-version=2024-08-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "system",
        "content": "You are an SAP S/4HANA Finance expert."
      },
      {
        "role": "user",
        "content": "Explain cost center accounting"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

### Streaming Responses

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Stream response for better UX
stream = client.chat.completions.create(
    model="sap-finance-gpt4o-mini",
    messages=[
        {"role": "system", "content": "You are an SAP Finance expert."},
        {"role": "user", "content": "Explain the Universal Journal"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

## Troubleshooting

### Issue: Authentication Error

```
Error: Unauthorized - Invalid API key
```

**Solution**: Check your API key and endpoint:
```bash
echo $AZURE_OPENAI_API_KEY
echo $AZURE_OPENAI_ENDPOINT
```

### Issue: Deployment Not Found

```
Error: The API deployment for this resource does not exist
```

**Solution**: Verify deployment name:
```bash
echo $DEPLOYMENT_NAME
# Should match your Azure OpenAI deployment name
```

### Issue: Rate Limit Exceeded

```
Error: Rate limit exceeded
```

**Solution**: 
- Increase TPM quota in Azure Portal
- Implement exponential backoff
- Use batch processing

## Best Practices

### 1. System Prompts

Always include a system prompt to set context:

```python
messages = [
    {
        "role": "system",
        "content": "You are an expert SAP S/4HANA Finance consultant "
                   "specializing in Financial Accounting (FI) and "
                   "Controlling (CO) modules."
    },
    {"role": "user", "content": "Your question here"}
]
```

### 2. Temperature Settings

- **Factual queries**: Use temperature 0.3-0.5 for consistent answers
- **Creative explanations**: Use temperature 0.7-0.9 for varied responses
- **Code generation**: Use temperature 0.0 for deterministic output

### 3. Token Management

- Monitor token usage to control costs
- Use max_tokens to prevent overly long responses
- Implement response caching for common queries

### 4. Error Handling

```python
try:
    response = client.chat.completions.create(...)
except openai.APIError as e:
    print(f"API Error: {e}")
except openai.RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    # Implement retry logic
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Additional Resources

- [Azure OpenAI SDK Documentation](https://learn.microsoft.com/azure/ai-services/openai/reference)
- [Setup Guide](../docs/SETUP_GUIDE.md)
- [Architecture Overview](../docs/ARCHITECTURE.md)
- [Use Cases](../docs/USE_CASES.md)

## Support

For issues or questions:
1. Check the [troubleshooting guide](../README.md#troubleshooting)
2. Review [Azure OpenAI documentation](https://learn.microsoft.com/azure/ai-services/openai/)
3. Open an issue on [GitHub](https://github.com/amitlals/Microsoft-Foundry-Fine-Tuning-Model-for-SAP-S-4HANA-Finance/issues)

---

**Last Updated**: December 2024  
**Version**: 1.0