# Architecture Overview

## System Architecture

This document describes the technical architecture of the SAP S/4HANA Finance fine-tuned model solution using Microsoft Azure AI Foundry.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Data Layer                                  │
│  ┌──────────────────┐         ┌──────────────────┐                 │
│  │  SAP Finance     │         │  Validation      │                 │
│  │  Training Data   │         │  Dataset         │                 │
│  │  (15 examples)   │         │  (5 examples)    │                 │
│  │  JSONL Format    │         │  JSONL Format    │                 │
│  └────────┬─────────┘         └────────┬─────────┘                 │
└───────────┼────────────────────────────┼───────────────────────────┘
            │                            │
            └────────────┬───────────────┘
                         │
                         │ Upload
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Azure AI Foundry Hub                              │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Data Management                              │ │
│  │  • Data validation and preprocessing                           │ │
│  │  • Azure Storage integration                                   │ │
│  │  • Format verification (JSONL)                                 │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                               │                                      │
│                               ▼                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                  Fine-Tuning Engine                             │ │
│  │                                                                  │ │
│  │  Base Model: GPT-4o-mini (2024-07-18)                          │ │
│  │  ├─ Pre-trained on general knowledge                           │ │
│  │  ├─ 128K context window                                        │ │
│  │  └─ Cost-effective inference                                   │ │
│  │                                                                  │ │
│  │  Fine-Tuning Method: LoRA (Low-Rank Adaptation)                │ │
│  │  ├─ Adapter layer training                                     │ │
│  │  ├─ Preserves base model knowledge                             │ │
│  │  ├─ Efficient parameter updates                                │ │
│  │  └─ Faster training convergence                                │ │
│  │                                                                  │ │
│  │  Hyperparameters:                                               │ │
│  │  ├─ Epochs: 3                                                  │ │
│  │  ├─ Batch size: Auto-optimized                                 │ │
│  │  ├─ Learning rate: Auto-optimized                              │ │
│  │  └─ Validation split: Separate file                            │ │
│  │                                                                  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                               │                                      │
│                               ▼                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                  Fine-Tuned Model                               │ │
│  │                                                                  │ │
│  │  Model: sap-finance-gpt4o-mini-v1                              │ │
│  │  ├─ SAP FI/CO domain expertise                                 │ │
│  │  ├─ Transaction code knowledge                                 │ │
│  │  ├─ Configuration guidance                                     │ │
│  │  └─ Best practices awareness                                   │ │
│  │                                                                  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                               │                                      │
└───────────────────────────────┼──────────────────────────────────────┘
                                │
                                │ Deploy
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Azure OpenAI Service                              │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                  Model Deployment                               │ │
│  │                                                                  │ │
│  │  Deployment Name: sap-finance-gpt4o-mini                       │ │
│  │  Type: Standard                                                 │ │
│  │  TPM (Tokens Per Minute): 10K - 100K                           │ │
│  │  Region: Available OpenAI regions                              │ │
│  │  Content Filters: Azure AI safety filters                      │ │
│  │                                                                  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                               │                                      │
└───────────────────────────────┼──────────────────────────────────────┘
                                │
                                │ Expose APIs
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API Layer                                       │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │   REST API   │    │  Python SDK  │    │   .NET SDK   │         │
│  │   HTTPS      │    │   openai     │    │  Azure.AI    │         │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘         │
│         │                   │                   │                  │
└─────────┼───────────────────┼───────────────────┼──────────────────┘
          │                   │                   │
          └─────────┬─────────┴───────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Application Layer                                 │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Web Apps    │  │ SAP Fiori    │  │  Power Apps  │             │
│  │  Custom UI   │  │ Extensions   │  │  Copilot     │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Teams Bots   │  │  Chatbots    │  │   Slack      │             │
│  │  Chat Apps   │  │  Support     │  │  Integration │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       End Users                                      │
│                                                                      │
│  • SAP Finance Consultants                                          │
│  • SAP End Users                                                    │
│  • Finance Team Members                                             │
│  • Training Participants                                            │
│  • Support Staff                                                    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Data Layer

**Training Data**:
- **Format**: JSONL (JSON Lines)
- **Structure**: Conversational format with system/user/assistant roles
- **Size**: 15 training examples, 5 validation examples
- **Coverage**: SAP FI/CO transaction codes, concepts, configurations

**Data Schema**:
```json
{
  "messages": [
    {
      "role": "system",
      "content": "System prompt defining assistant behavior"
    },
    {
      "role": "user", 
      "content": "User question about SAP Finance"
    },
    {
      "role": "assistant",
      "content": "Expert response with SAP knowledge"
    }
  ]
}
```

**Quality Assurance**:
- Manual verification against SAP documentation
- Peer review by SAP Finance experts
- Validation script for format compliance
- Token count estimation

### 2. Azure AI Foundry Hub

**Components**:

**Data Management**:
- Azure Storage Account for dataset storage
- Data validation and preprocessing
- Version control for datasets
- Access control and security

**Fine-Tuning Engine**:
- GPU-accelerated training infrastructure
- Automated hyperparameter optimization
- Real-time training metrics
- Model versioning and management

**Monitoring**:
- Training loss curves
- Validation metrics
- Resource utilization
- Cost tracking

### 3. Base Model: GPT-4o-mini

**Characteristics**:
- **Model Family**: GPT-4 optimized
- **Size**: Mini variant (cost-effective)
- **Context Window**: 128K tokens
- **Training Cutoff**: September 2023
- **Strengths**:
  - Strong reasoning capabilities
  - Good instruction following
  - Efficient inference
  - Lower cost than full GPT-4

### 4. Fine-Tuning: LoRA (Low-Rank Adaptation)

**Technical Approach**:

```
Base Model (Frozen)
    │
    ├─── Layer 1 ───┬─── LoRA Adapter A (trainable)
    │               └─── LoRA Adapter B (trainable)
    │
    ├─── Layer 2 ───┬─── LoRA Adapter A (trainable)
    │               └─── LoRA Adapter B (trainable)
    │
    └─── ... (more layers)

Final Prediction = Base Model Output + LoRA Adapters
```

**LoRA Parameters**:
- **Rank (r)**: Low-rank decomposition dimension (typically 8-16)
- **Alpha**: Scaling factor for adapter weights
- **Target Modules**: Attention and feed-forward layers
- **Dropout**: Regularization (typically 0.1)

**Advantages**:
- 90% reduction in trainable parameters
- 60% faster training
- 70% cost reduction
- Same inference speed as base model
- Preserves general knowledge

### 5. Azure OpenAI Service

**Deployment Configuration**:

**Compute Resources**:
- Auto-scaling based on load
- Multi-region availability
- High availability (99.9% SLA)
- Load balancing

**Security**:
- Managed identity authentication
- VNet integration support
- Private endpoints
- Azure RBAC integration
- Content filtering (Azure AI safety)

**Monitoring**:
- Azure Monitor integration
- Application Insights
- Custom metrics and alerts
- Token usage tracking

### 6. API Layer

**REST API**:
```
Endpoint: https://{resource}.openai.azure.com/openai/deployments/{deployment}/chat/completions
Method: POST
API Version: 2024-08-01-preview
Authentication: API Key or Managed Identity
```

**Request Schema**:
```json
{
  "messages": [
    {"role": "system", "content": "System prompt"},
    {"role": "user", "content": "User query"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000,
  "top_p": 0.95,
  "frequency_penalty": 0,
  "presence_penalty": 0
}
```

**SDKs Available**:
- Python (openai package)
- .NET (Azure.AI.OpenAI)
- JavaScript/TypeScript (openai)
- Java (Azure SDK)

### 7. Application Layer

**Integration Patterns**:

**1. Direct Integration**:
```python
from openai import AzureOpenAI

client = AzureOpenAI(...)
response = client.chat.completions.create(...)
```

**2. SAP Fiori Extension**:
- Embed chat widget in Fiori apps
- Context-aware assistance
- Transaction-specific help

**3. Power Platform**:
- Power Apps with Azure OpenAI connector
- Power Automate for workflow automation
- Power BI for analytics

**4. Microsoft Teams**:
- Teams bot framework
- Adaptive cards for rich responses
- Proactive notifications

## Data Flow

### Training Phase

```
1. Dataset Upload
   ├─ User uploads JSONL files to Azure AI Foundry
   └─ System validates format and structure

2. Training Job Creation
   ├─ Select base model (GPT-4o-mini)
   ├─ Configure hyperparameters
   └─ Submit to training queue

3. Training Execution
   ├─ Load base model
   ├─ Initialize LoRA adapters
   ├─ Train on SAP Finance data
   ├─ Validate after each epoch
   └─ Save checkpoints

4. Model Evaluation
   ├─ Calculate validation metrics
   ├─ Generate loss curves
   └─ Assess convergence

5. Model Registration
   ├─ Register fine-tuned model
   ├─ Tag with metadata
   └─ Make available for deployment
```

### Inference Phase

```
1. User Request
   ├─ Application sends query to Azure OpenAI
   └─ Includes conversation history

2. API Gateway
   ├─ Authenticate request
   ├─ Check rate limits
   └─ Route to deployment

3. Model Inference
   ├─ Load fine-tuned model + LoRA adapters
   ├─ Process input through model
   ├─ Apply temperature and sampling
   └─ Generate response

4. Post-Processing
   ├─ Apply content filters
   ├─ Format response
   └─ Log metrics

5. Response Delivery
   ├─ Return to application
   └─ Display to user
```

## Security Architecture

### Authentication & Authorization

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Azure AD           │
│  - User identity    │
│  - MFA              │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Azure RBAC         │
│  - Role assignment  │
│  - Permissions      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Azure OpenAI       │
│  - API Key / MI     │
│  - Resource access  │
└─────────────────────┘
```

### Data Protection

- **Data at Rest**: 
  - Azure Storage encryption (256-bit AES)
  - Model weights encrypted
  - Managed keys (Azure Key Vault)

- **Data in Transit**:
  - TLS 1.2+ encryption
  - HTTPS only
  - Certificate validation

- **Data Privacy**:
  - No training data retention after fine-tuning
  - Customer data isolation
  - GDPR compliance

### Content Filtering

```
User Input
    │
    ▼
┌─────────────────────┐
│  Input Filter       │
│  - Harmful content  │
│  - PII detection    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Model Inference    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Output Filter      │
│  - Harmful content  │
│  - Jailbreak detect │
└──────┬──────────────┘
       │
       ▼
   Response
```

## Scalability & Performance

### Horizontal Scaling

- Auto-scaling based on request volume
- Multiple deployment regions
- Load balancing across instances
- Queue management for burst traffic

### Performance Optimization

**Latency Targets**:
- P50: < 2 seconds
- P95: < 5 seconds
- P99: < 10 seconds

**Optimization Techniques**:
- Prompt caching for common queries
- Streaming responses for better UX
- Batch processing for bulk requests
- Connection pooling

### Capacity Planning

**Tokens Per Minute (TPM) Quotas**:
- Development: 10K TPM
- Staging: 50K TPM
- Production: 100K+ TPM

**Cost Management**:
- Monitor token usage
- Set budget alerts
- Optimize prompt lengths
- Cache frequent queries

## Monitoring & Observability

### Key Metrics

**Model Performance**:
- Response accuracy
- Token usage per request
- Average response time
- Error rate

**System Health**:
- API availability (%)
- Request latency (ms)
- Throughput (requests/sec)
- Resource utilization

**Business Metrics**:
- User satisfaction scores
- Query categories
- Feature adoption
- Cost per query

### Logging

```
Request Logs:
├─ Timestamp
├─ User/Application ID
├─ Query text (sanitized)
├─ Response summary
├─ Tokens used
├─ Latency
└─ Status code

Error Logs:
├─ Error type
├─ Error message
├─ Stack trace
├─ Context
└─ Remediation steps
```

### Alerting

- High error rate (> 5%)
- Elevated latency (> 5s P95)
- Low availability (< 99%)
- Budget threshold exceeded
- Unusual usage patterns

## Disaster Recovery

### Backup Strategy

- **Model Artifacts**: Daily backups to geo-redundant storage
- **Configuration**: Version controlled in Git
- **Training Data**: Immutable storage with versioning

### Failover

- Multi-region deployment
- Automatic failover to secondary region
- RTO (Recovery Time Objective): < 1 hour
- RPO (Recovery Point Objective): < 24 hours

## Compliance & Governance

### Regulatory Compliance

- GDPR (General Data Protection Regulation)
- SOC 2 Type II
- ISO 27001
- HIPAA (if processing health data)

### Model Governance

- Model card documentation
- Version control and lineage
- Change management process
- Regular model audits
- Bias and fairness testing

## Cost Architecture

### Cost Breakdown

**Training Costs** (One-time):
- Fine-tuning compute: $50-$200
- Storage: $1-$5/month
- Data transfer: Minimal

**Inference Costs** (Ongoing):
- Input tokens: $0.00015 per 1K tokens
- Output tokens: $0.0006 per 1K tokens
- Model hosting: Included in token pricing

**Infrastructure Costs**:
- Azure AI Foundry Hub: Free tier available
- Storage: ~$0.02 per GB/month
- Networking: Minimal for typical usage

### Cost Optimization

- Use prompt compression techniques
- Implement response caching
- Batch similar queries
- Monitor and optimize token usage
- Use appropriate TPM quotas

---

**Last Updated**: December 2024  
**Version**: 1.0
