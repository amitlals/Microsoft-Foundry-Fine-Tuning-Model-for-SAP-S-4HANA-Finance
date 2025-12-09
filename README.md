# Microsoft Foundry Fine-Tuning Model for SAP S/4HANA Finance

![SAP](https://img.shields.io/badge/SAP-S%2F4HANA-blue)
![Azure](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4)
![GPT-4o-mini](https://img.shields.io/badge/Model-GPT--4o--mini-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🎯 Executive Summary

This comprehensive demo showcases how to fine-tune a **GPT-4o-mini** model using **Microsoft Azure AI Foundry's** portal-based (no-code) interface with an SAP Finance-specific dataset. The fine-tuned model understands SAP FI/CO terminology, transaction codes, and provides domain-specific responses for financial operations.

**Key Outcomes**:
- ✅ **Domain Specialization**: Adapt GPT-4o-mini for SAP S/4HANA Finance domain
- ✅ **No-Code Approach**: Use Azure AI Foundry portal without programming
- ✅ **Production-Ready**: Deploy fine-tuned model as Azure OpenAI endpoint
- ✅ **Cost-Effective**: Leverage LoRA for efficient parameter fine-tuning

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Dataset](#dataset)
- [Fine-Tuning Process](#fine-tuning-process)
- [Deployment](#deployment)
- [Testing & Validation](#testing--validation)
- [Use Cases](#use-cases)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

### What is SAP S/4HANA Finance?

SAP S/4HANA Finance is the core financial management module encompassing:
- **FI (Financial Accounting)**: General Ledger, AR, AP, Asset Accounting
- **CO (Controlling)**: Cost Center Accounting, Profit Center, Internal Orders
- **New G/L**: Universal Journal, Document Splitting, Real-time Reporting

### Why Fine-Tune for SAP Finance?

**Challenge**: Generic LLMs lack deep knowledge of:
- SAP-specific transaction codes (FB50, FS00, F110, etc.)
- FI/CO terminology and concepts
- Best practices for SAP financial processes
- Configuration and troubleshooting guidance

**Solution**: Fine-tune GPT-4o-mini with SAP Finance domain data to create a specialized assistant that:
- Understands SAP terminology and transaction codes
- Provides accurate configuration guidance
- Explains complex SAP Finance concepts
- Assists with troubleshooting and best practices

### Microsoft Azure AI Foundry

Azure AI Foundry (formerly Azure AI Studio) is Microsoft's unified platform for building AI solutions:
- **No-Code Interface**: Portal-based fine-tuning without programming
- **Enterprise-Grade**: Security, compliance, and governance built-in
- **Integrated**: Seamless Azure OpenAI Service integration
- **Scalable**: Production-ready deployment infrastructure

## 🏗️ Architecture

### Solution Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Azure AI Foundry Hub                      │
│                                                              │
│  ┌────────────────┐         ┌──────────────────┐           │
│  │   SAP Finance  │         │   GPT-4o-mini    │           │
│  │   Training     │────────▶│   Base Model     │           │
│  │   Dataset      │         │                  │           │
│  │   (JSONL)      │         └────────┬─────────┘           │
│  └────────────────┘                  │                     │
│                                      │                     │
│                           ┌──────────▼──────────┐          │
│                           │   Fine-Tuning       │          │
│                           │   (LoRA Adaptation) │          │
│                           └──────────┬──────────┘          │
│                                      │                     │
│                           ┌──────────▼──────────┐          │
│                           │  Fine-Tuned Model   │          │
│                           │  sap-finance-v1     │          │
│                           └──────────┬──────────┘          │
│                                      │                     │
└──────────────────────────────────────┼─────────────────────┘
                                       │
                            ┌──────────▼──────────┐
                            │  Azure OpenAI       │
                            │  Deployment         │
                            └──────────┬──────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
              ┌─────▼─────┐     ┌─────▼─────┐     ┌─────▼─────┐
              │  REST API │     │ Python SDK│     │ Fiori Apps│
              └───────────┘     └───────────┘     └───────────┘
```

### Technical Approach

**Fine-Tuning Method**: Low-Rank Adaptation (LoRA)
- Efficient parameter updates
- Preserves base model knowledge
- Reduces training time and cost
- Maintains model quality

**Data Format**: JSONL (JSON Lines)
- Chat format with system/user/assistant roles
- SAP FI/CO domain-specific conversations
- 15+ training examples, 5+ validation examples

## ✨ Features

### Model Capabilities

After fine-tuning, the model can:

✅ **Explain SAP Transaction Codes**
- FB50, F-02, FS00, FB60, F110, etc.
- Usage context and best practices
- Step-by-step guidance

✅ **Understand SAP Finance Concepts**
- Document splitting
- Cost center accounting
- Profit center accounting
- Universal Journal
- Payment programs

✅ **Provide Configuration Guidance**
- Account determination
- Posting key configuration
- Period-end closing procedures
- Integration scenarios

✅ **Assist with Troubleshooting**
- Common error messages
- Configuration issues
- Best practices recommendations

### Integration Options

- **Azure OpenAI SDK** (Python, .NET, Java, Node.js)
- **REST API** (Any language/platform)
- **SAP Fiori Apps** (Custom extensions)
- **Microsoft Power Platform** (Power Apps, Power Automate)
- **Teams Bots** (Microsoft Teams integration)

## 📦 Prerequisites

### Azure Requirements

1. **Azure Subscription** with sufficient credits
2. **Azure AI Foundry Hub** (create in Azure Portal)
3. **Azure OpenAI Service** resource
4. **GPT-4o-mini model access** in your region

### Permissions Required

- `Cognitive Services OpenAI Contributor`
- `Azure AI Developer`
- `Storage Blob Data Contributor` (for datasets)

### Tools & Skills

- Web browser (for no-code portal access)
- Basic understanding of:
  - SAP Finance concepts (helpful but not required)
  - Azure portal navigation
  - JSON data format

### Cost Considerations

**Estimated Costs**:
- Fine-tuning: $50-$200 (one-time, depends on data size)
- Model hosting: $0.50-$2.00 per hour
- Inference: Standard GPT-4o-mini pricing

💡 **Tip**: Use Azure Cost Management to monitor and set budgets

## 🚀 Quick Start

### Step 1: Clone Repository

```bash
git clone https://github.com/amitlals/Microsoft-Foundry-Fine-Tuning-Model-for-SAP-S-4HANA-Finance.git
cd Microsoft-Foundry-Fine-Tuning-Model-for-SAP-S-4HANA-Finance
```

### Step 2: Review Training Data

Explore the provided datasets:
- `data/sap_finance_training.jsonl` - Training examples (15 conversations)
- `data/sap_finance_validation.jsonl` - Validation examples (5 conversations)

### Step 3: Follow Setup Guide

Detailed step-by-step instructions: **[docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)**

Quick overview:
1. Access Azure AI Foundry portal
2. Create Hub and Project
3. Upload training data
4. Configure fine-tuning parameters
5. Monitor training progress
6. Deploy fine-tuned model
7. Test with SAP Finance queries

### Step 4: Test the Model

```python
import openai

client = openai.AzureOpenAI(
    api_key="your-api-key",
    api_version="2024-08-01-preview",
    azure_endpoint="https://your-resource.openai.azure.com"
)

response = client.chat.completions.create(
    model="sap-finance-gpt4o-mini",
    messages=[
        {"role": "system", "content": "You are an SAP S/4HANA Finance expert."},
        {"role": "user", "content": "What is transaction code FB50?"}
    ]
)

print(response.choices[0].message.content)
```

## 📊 Dataset

### Training Data Structure

Each line in the JSONL file contains a conversation:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are an expert SAP S/4HANA Finance consultant specializing in Financial Accounting (FI) and Controlling (CO) modules."
    },
    {
      "role": "user",
      "content": "What is transaction code FB50?"
    },
    {
      "role": "assistant",
      "content": "FB50 is the SAP transaction code used to post G/L account documents directly in Financial Accounting (FI)..."
    }
  ]
}
```

### Dataset Coverage

**SAP FI Topics** (15 training examples):
- Transaction codes: FB50, F-02, FB60, FS00, F110
- Document splitting and New G/L
- Cost center accounting
- Payment program automation
- Profit center accounting
- Inventory account determination
- Cost elements vs G/L accounts
- Month-end closing procedures
- Universal Journal (S/4HANA)

**Validation Topics** (5 examples):
- Customer invoice posting (FB70)
- Company code creation
- Asset class configuration
- Posting keys explanation

### Data Quality Guidelines

✅ **Accurate**: All information verified against SAP documentation
✅ **Comprehensive**: Detailed explanations with examples
✅ **Consistent**: Standardized format and terminology
✅ **Domain-Specific**: Focuses on SAP Finance domain

## 🎓 Fine-Tuning Process

### Portal-Based Workflow (No-Code)

**1. Data Preparation**
- Upload JSONL files to Azure AI Foundry
- Validate format and content
- Split into training and validation sets

**2. Model Selection**
- Choose GPT-4o-mini as base model
- Select latest version (2024-07-18 or newer)

**3. Hyperparameter Configuration**
- **Epochs**: 3 (recommended for domain adaptation)
- **Batch size**: Auto (system optimizes)
- **Learning rate**: Auto (system optimizes)
- **Suffix**: `sap-finance-v1`

**4. Training Execution**
- Submit fine-tuning job
- Monitor in real-time dashboard
- Typical duration: 20-60 minutes

**5. Validation & Metrics**
- Review training loss curves
- Check validation performance
- Verify convergence

### LoRA (Low-Rank Adaptation)

Microsoft Foundry uses LoRA for efficient fine-tuning:

**Benefits**:
- ⚡ Faster training (60% reduction)
- 💰 Lower cost (fewer compute resources)
- 🎯 Better quality (preserves base model)
- 🔧 Easier updates (can combine multiple LoRAs)

**How it works**:
- Freezes base model parameters
- Adds small trainable adapter layers
- Updates only adapter weights
- Final model = Base + Adapter

## 🌐 Deployment

### Azure OpenAI Endpoint

After training, deploy to Azure OpenAI:

**Deployment Configuration**:
- **Name**: `sap-finance-gpt4o-mini`
- **Type**: Standard deployment
- **TPM (Tokens Per Minute)**: 10K-100K (based on needs)
- **Content Filter**: Default Azure AI safety filters

### Access Patterns

**1. REST API**
```bash
curl https://your-resource.openai.azure.com/openai/deployments/sap-finance-gpt4o-mini/chat/completions?api-version=2024-08-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: your-api-key" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are an SAP S/4HANA Finance expert."},
      {"role": "user", "content": "Explain cost center accounting"}
    ]
  }'
```

**2. Python SDK**
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="your-api-key",
    api_version="2024-08-01-preview",
    azure_endpoint="https://your-resource.openai.azure.com"
)

response = client.chat.completions.create(
    model="sap-finance-gpt4o-mini",
    messages=[
        {"role": "system", "content": "You are an SAP S/4HANA Finance expert."},
        {"role": "user", "content": "How does F110 payment program work?"}
    ]
)
```

**3. Power Platform Integration**
Use Azure OpenAI connector in Power Automate for SAP process automation.

## 🧪 Testing & Validation

### Test Scenarios

**Transaction Code Knowledge**:
```
Q: What is the difference between FB50 and F-02?
Expected: Detailed comparison with recommendations
```

**Process Guidance**:
```
Q: How do I run month-end closing in SAP?
Expected: Step-by-step procedure with transaction codes
```

**Configuration Help**:
```
Q: How do I configure automatic account determination for inventory?
Expected: OBYC configuration steps with examples
```

**Troubleshooting**:
```
Q: Why is my payment program F110 failing?
Expected: Common issues and solutions
```

### Quality Metrics

Monitor these KPIs:
- **Accuracy**: Correct SAP terminology and processes
- **Completeness**: Comprehensive answers with details
- **Relevance**: Domain-specific, not generic responses
- **Latency**: Response time (<3 seconds preferred)

### Evaluation Process

1. **Baseline Testing**: Compare with non-fine-tuned GPT-4o-mini
2. **Subject Matter Expert Review**: SAP Finance experts validate
3. **User Acceptance Testing**: Real users test with actual queries
4. **Continuous Monitoring**: Track production performance

## 💼 Use Cases

### 1. SAP Finance Helpdesk

**Scenario**: Self-service support for SAP users
- Users ask questions about transaction codes
- Model provides instant, accurate answers
- Reduces helpdesk ticket volume

### 2. Training & Onboarding

**Scenario**: New SAP Finance team members
- Interactive learning experience
- On-demand explanations
- Best practices guidance

### 3. Process Documentation

**Scenario**: Dynamic documentation assistant
- Context-aware procedure guidance
- Step-by-step instructions
- Configuration examples

### 4. Integration with SAP Fiori

**Scenario**: Embedded AI assistant in Fiori apps
- Contextual help within transactions
- Process guidance overlay
- Error resolution assistance

### 5. Audit & Compliance

**Scenario**: Compliance team training
- Understanding SAP controls
- Configuration validation
- Best practice adherence

## 📚 Best Practices

### Training Data

✅ **Quality over Quantity**: 15-50 high-quality examples better than 1000 poor ones
✅ **Diverse Topics**: Cover breadth of SAP Finance domain
✅ **Accurate Content**: Verify all information against SAP documentation
✅ **Consistent Format**: Maintain standard conversation structure
✅ **Regular Updates**: Refresh with new SAP updates and features

### Fine-Tuning Configuration

✅ **Start with 3 epochs**: Good balance for domain adaptation
✅ **Use validation set**: Monitor for overfitting
✅ **Monitor loss curves**: Should decrease steadily
✅ **Test iteratively**: Fine-tune, test, refine, repeat

### Production Deployment

✅ **Set appropriate TPM limits**: Based on expected usage
✅ **Implement content filters**: Use Azure AI safety features
✅ **Monitor costs**: Track token usage and API calls
✅ **Version control**: Maintain multiple model versions
✅ **Gradual rollout**: Test with limited users first

### Model Management

✅ **Regular retraining**: Update with new SAP features quarterly
✅ **Performance monitoring**: Track accuracy and user satisfaction
✅ **Feedback loop**: Collect user feedback for improvements
✅ **A/B testing**: Compare model versions

## 🔧 Troubleshooting

### Common Issues

**Issue**: Fine-tuning job fails
```
Solution:
- Validate JSONL format (use online validator)
- Check file size limits (max 1GB)
- Verify required fields in each message
- Review error logs in Azure portal
```

**Issue**: Model provides generic responses
```
Solution:
- Increase training examples (aim for 20+)
- Add more diverse SAP Finance topics
- Increase epochs to 5
- Verify training data quality
```

**Issue**: High latency in responses
```
Solution:
- Increase TPM quota
- Use async processing for long responses
- Implement caching for common queries
- Consider response streaming
```

**Issue**: Deployment timeout
```
Solution:
- Check Azure OpenAI quota limits
- Try different Azure region
- Verify subscription status
- Contact Azure support
```

### Getting Help

- 📖 [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- 📖 [Azure OpenAI Fine-tuning Guide](https://learn.microsoft.com/azure/ai-services/openai/how-to/fine-tuning)
- 💬 [GitHub Issues](https://github.com/amitlals/Microsoft-Foundry-Fine-Tuning-Model-for-SAP-S-4HANA-Finance/issues)
- 🎫 [Azure Support Portal](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Add Training Examples

1. Fork the repository
2. Add new examples to `data/sap_finance_training.jsonl`
3. Follow existing format and quality standards
4. Submit pull request with description

### Improve Documentation

- Fix typos or unclear instructions
- Add screenshots or diagrams
- Enhance troubleshooting guide
- Translate to other languages

### Share Use Cases

- Document your implementation
- Share lessons learned
- Provide performance metrics
- Suggest improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- SAP Community for knowledge sharing
- Microsoft Azure AI team for Foundry platform
- OpenAI for GPT-4o-mini model
- Contributors and early adopters

## 📞 Contact

- **Author**: Amit Lal
- **Repository**: [GitHub](https://github.com/amitlals/Microsoft-Foundry-Fine-Tuning-Model-for-SAP-S-4HANA-Finance)
- **Issues**: [Report Issues](https://github.com/amitlals/Microsoft-Foundry-Fine-Tuning-Model-for-SAP-S-4HANA-Finance/issues)

## 🗺️ Roadmap

### Current Version (v1.0)
- ✅ Core SAP FI/CO training data
- ✅ GPT-4o-mini fine-tuning
- ✅ No-code Azure AI Foundry setup
- ✅ Comprehensive documentation

### Planned Enhancements (v2.0)
- 🔄 Additional SAP modules (MM, SD, PP)
- 🔄 Multilingual support (German, Spanish, French)
- 🔄 Advanced troubleshooting scenarios
- 🔄 Integration examples with SAP systems
- 🔄 Automated testing framework
- 🔄 Performance benchmarking tools

---

**⭐ Star this repository** if you find it helpful!

**🔔 Watch for updates** on new features and improvements!

**🍴 Fork to customize** for your organization's needs!
