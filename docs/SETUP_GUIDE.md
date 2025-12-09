# Microsoft Foundry Fine-Tuning Setup Guide
## SAP S/4HANA Finance Domain Adaptation

### Prerequisites

Before starting the fine-tuning process, ensure you have:

1. **Azure Subscription** with active credits
2. **Azure AI Foundry Hub** (formerly Azure AI Studio) access
3. **Access to GPT-4o-mini model** in your Azure region
4. **Appropriate RBAC permissions**:
   - Cognitive Services OpenAI Contributor
   - Azure AI Developer
5. **Training data** in JSONL format (provided in this repository)

### Azure Resources Required

- **Azure AI Foundry Hub**: Central workspace for managing AI projects
- **Azure OpenAI Service**: Host for GPT-4o-mini base model
- **Azure Storage Account**: For storing training datasets
- **Compute Resources**: Automatically provisioned during fine-tuning

### Estimated Costs

Fine-tuning costs depend on:
- Training tokens processed
- Model hosting hours
- Inference requests

**Typical costs for SAP Finance fine-tuning**:
- Training: $50-$200 (one-time)
- Hosting: $0.50-$2.00 per hour
- Inference: Standard GPT-4o-mini pricing

## Step-by-Step Setup

### Step 1: Access Azure AI Foundry

1. Navigate to [Azure AI Foundry Portal](https://ai.azure.com)
2. Sign in with your Azure credentials
3. Select or create a new Hub:
   - Click **"+ New hub"**
   - Name: `sap-finance-ai-hub`
   - Region: Choose region with GPT-4o-mini availability
   - Subscription: Select your Azure subscription

### Step 2: Create a Project

1. Within your hub, click **"+ New project"**
2. Configure project settings:
   - **Name**: `sap-s4hana-finance-assistant`
   - **Description**: SAP FI/CO specialized model through fine-tuning
3. Click **"Create"** and wait for provisioning

### Step 3: Prepare Training Data

1. Download the training dataset from this repository:
   - `data/sap_finance_training.jsonl`
   - `data/sap_finance_validation.jsonl`

2. Review the data format (each line is a JSON object):
```json
{"messages": [{"role": "system", "content": "You are an SAP S/4HANA Finance expert..."}, {"role": "user", "content": "What is FB50?"}, {"role": "assistant", "content": "FB50 is the transaction code..."}]}
```

### Step 4: Upload Training Data

1. In your project, navigate to **"Data + indexes"** → **"Data"**
2. Click **"+ New data"**
3. Select **"Upload files"**
4. Upload both JSONL files:
   - Training: `sap_finance_training.jsonl`
   - Validation: `sap_finance_validation.jsonl`
5. Data type: Select **"Fine-tuning"**
6. Click **"Create"**

### Step 5: Start Fine-Tuning (No-Code)

1. Navigate to **"Fine-tuning"** in the left menu
2. Click **"+ Fine-tune model"**
3. Select base model:
   - **Model**: `gpt-4o-mini` (2024-07-18 or later)
   - Click **"Confirm"**

4. Configure training:
   - **Training data**: Select your uploaded training file
   - **Validation data**: Select your uploaded validation file (optional but recommended)
   
5. Set fine-tuning parameters:
   - **Suffix**: `sap-finance-v1`
   - **Epochs**: 3 (recommended for domain adaptation)
   - **Batch size**: Auto (recommended)
   - **Learning rate multiplier**: Auto (recommended)

6. Review and create:
   - Review all settings
   - Click **"Submit"** to start fine-tuning

### Step 6: Monitor Training

1. Training will appear in the **"Fine-tuning"** dashboard
2. Monitor progress:
   - **Status**: Queued → Running → Succeeded
   - **Metrics**: Training loss, validation loss
   - **Duration**: Typically 20-60 minutes

3. Review training metrics when complete:
   - Training loss should decrease steadily
   - Validation loss indicates generalization
   - Look for convergence without overfitting

### Step 7: Deploy Fine-Tuned Model

1. Once training succeeds, click on your fine-tuned model
2. Click **"Deploy"**
3. Configure deployment:
   - **Deployment name**: `sap-finance-gpt4o-mini`
   - **Deployment type**: Standard
   - **Tokens per minute rate limit**: 10K (adjust based on needs)
   - **Content filter**: Default (Azure AI content safety)

4. Click **"Deploy"** and wait for provisioning

### Step 8: Test the Model

1. Navigate to **"Playground"** → **"Chat"**
2. Select your deployed model: `sap-finance-gpt4o-mini`
3. Test with SAP Finance queries:

**Example Test 1**:
```
User: What is the difference between FB50 and F-02?
```

**Example Test 2**:
```
User: Explain the document splitting process in New GL
```

**Example Test 3**:
```
User: How do I post a vendor invoice with tax code?
```

### Step 9: Integrate with Applications

After successful testing, integrate using:

**Option 1: Azure OpenAI SDK**
```python
import openai

client = openai.AzureOpenAI(
    api_key="your-api-key",
    api_version="2024-08-01-preview",
    azure_endpoint="https://your-resource.openai.azure.com"
)

response = client.chat.completions.create(
    model="sap-finance-gpt4o-mini",  # Your deployment name
    messages=[
        {"role": "system", "content": "You are an SAP S/4HANA Finance expert."},
        {"role": "user", "content": "What is transaction code FB50?"}
    ]
)
print(response.choices[0].message.content)
```

**Option 2: REST API**
```bash
curl https://your-resource.openai.azure.com/openai/deployments/sap-finance-gpt4o-mini/chat/completions?api-version=2024-08-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: your-api-key" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are an SAP S/4HANA Finance expert."},
      {"role": "user", "content": "What is FB50?"}
    ]
  }'
```

## Validation and Quality Assurance

### Post-Deployment Testing

1. **Accuracy Testing**: Verify responses for common SAP FI/CO queries
2. **Terminology Check**: Ensure proper use of SAP-specific terms
3. **Transaction Code Knowledge**: Test major T-codes (FB50, F-02, FS00, etc.)
4. **Domain Context**: Validate understanding of FI/CO concepts

### Evaluation Metrics

Monitor these metrics:
- **Response Accuracy**: Correct SAP terminology and processes
- **Latency**: Response time (should be <3 seconds)
- **Token Usage**: Efficiency of responses
- **User Satisfaction**: Feedback from SAP Finance users

### Iteration and Improvement

1. Collect user feedback on model responses
2. Identify gaps in domain knowledge
3. Enhance training dataset with new examples
4. Re-train with updated data for improved accuracy

## Troubleshooting

### Common Issues

**Issue**: Fine-tuning job fails
- **Solution**: Check data format, ensure JSONL is valid, verify file size limits

**Issue**: Model deployment timeout
- **Solution**: Check quota limits, try different region, contact support

**Issue**: Poor model accuracy
- **Solution**: Review training data quality, increase training examples, adjust epochs

**Issue**: High latency
- **Solution**: Increase TPM quota, optimize prompts, consider caching

### Support Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Azure OpenAI Fine-tuning Guide](https://learn.microsoft.com/azure/ai-services/openai/how-to/fine-tuning)
- [Azure Support Portal](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade)

## Next Steps

1. ✅ Complete fine-tuning setup
2. ✅ Test model with SAP Finance queries
3. 📊 Gather baseline metrics
4. 🔄 Iterate based on feedback
5. 🚀 Deploy to production environment
6. 📈 Monitor and optimize performance

---

**Last Updated**: December 2024  
**Version**: 1.0
