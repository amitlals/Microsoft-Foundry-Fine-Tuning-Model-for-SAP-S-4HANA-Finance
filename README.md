Microsoft Foundry Fine-Tuning Model for SAP S/4HANA Finance 
SAP S/4HANA Finance Domain Adaptation | No-Code Approach
Executive Summary
This demo showcases how to fine-tune a GPT-4o-mini model using Microsoft Foundry's portal-based (no-code) interface with an SAP Finance-specific dataset. The fine-tuned model will understand SAP FI/CO terminology, transaction codes, and provide domain-specific responses for financial operations.
SAP Finance AI Agent Powered by Fine-tuned LLM
Business Problem
Finance teams leveraging SAP S/4HANA or SAP ERP require immediate, accurate answers related to transaction codes, GL accounts, cost centers, and various financial processes. Standard AI models often lack the specialized SAP domain expertise needed, leading organizations to invest heavily in additional training or hire external consultants—often with limited efficiency and less productive outcomes. Furthermore, these generic models are prone to generating inaccurate or irrelevant information (hallucinations). Fine-tuning large language models (LLMs) with SAP-specific data significantly enhances accuracy, reliability, and overall productivity for finance operations.
Solution
A fine-tuned model that:
•	Understands SAP FI/CO module terminology and concepts
•	Provides accurate transaction code guidance (FB01, F-28, etc.)
•	Explains GL account structures and posting logic
•	Assists with month-end close procedures
•	Responds in SAP-native terminology customers expect
Prerequisites
1.	Azure subscription with Azure AI Foundry access
2.	Azure AI User role assigned (required for fine-tuning)
3.	Region with fine-tuning support (East US 2, Sweden Central, or North Central US recommended)
4.	JSONL training file (provided in attachment 50 scnearios)
5.	Understanding of SAP FI/CO basics for demo narrative
 
Step-by-Step Demo Guide (Portal Only)
Phase 1: Setup Azure AI Foundry Project
1.	Navigate to portal.azure.com → Azure AI Foundry
2.	Create a new Project (or use existing Hub/Project)
3.	Ensure region supports fine-tuning (check Model Catalog → Fine-tuning filter)
4.	Verify Azure AI User role is assigned to your account
Phase 2: Upload Training Data
•	Go to Fine-tuning section in left sidebar
•	Click '+ Fine-tune model'
•	Select base model: gpt-4o-mini-2024-07-18 (recommended for cost-effective demos)
•	Upload training file: sap_finance_training.jsonl
•	Upload validation file: sap_finance_validation.jsonl (optional but recommended)
Phase 3: Configure Fine-Tuning Job
Recommended settings for demo:
Parameter	Recommended Value
Epochs	3-5 (start with 3 for demo speed)
Batch Size	Auto (let system optimize)
Learning Rate Multiplier	Auto (default) or 0.1 for conservative
Suffix	sap-finance-demo
Phase 4: Monitor Training
•	Training typically takes 15-45 minutes for this dataset size
•	Monitor training loss curve in the portal
•	Check validation loss to ensure no overfitting
•	Status will change: Pending → Running → Succeeded
Phase 5: Deploy Fine-Tuned Model
•	Once training completes, click 'Deploy'
•	Choose deployment name: sap-finance-assistant
•	Select capacity (1 TPM is sufficient for demo)
•	Deployment takes ~5 minutes
 
How Low‑Rank Adaptation (LoRA) Fine‑Tuning Works
Low-Rank Adaptation (LoRA) on Microsoft Foundry is a technique that makes it easier and cheaper to fine-tune large language models for specific tasks or industries. Imagine a huge encyclopedia (the base model) that already knows a lot. Instead of rewriting or changing the whole encyclopedia for each new topic, LoRA lets you add a few special notes or sticky tabs (small trainable pieces) in certain sections. During training, only these notes are updated, while the rest of the encyclopedia stays the same. This approach saves time and computer power, lowers costs, and preserves the model’s general knowledge, while allowing it to learn new, specialized information efficiently.
The fine‑tuning job learns only these additional parameters, which means:
• Far fewer trainable parameters → lower GPU memory and faster training.
• Costs are much lower than full model fine‑tuning.
• The base model’s general knowledge is preserved while SAP‑specific behavior is overlaid.

In practice, a small dataset (tens to low hundreds of examples) can yield a very useful domain‑adapted model.
Prompt Engineering and Behavior
System Prompt Pattern
Recommended system message for the deployed model:
"You are an SAP Finance (FI/CO) expert assistant. Answer questions about SAP S/4HANA Finance using accurate SAP terminology and transaction codes. Be concise, factual, and explicit about assumptions. When relevant, provide step-by-step instructions and mention key configuration points or dependencies. Clearly indicate when a process may differ based on system version (e.g., ECC vs. S/4HANA) or user roles. If you are unsure, state your uncertainty and suggest possible resources such as SAP Help, official documentation, or transaction codes for further verification. Use examples where appropriate, and clarify when alternative transactions or methods exist. Prioritize clarity and accuracy to support users in real-world SAP Finance scenarios."
Example – Pre‑Trained vs Fine‑Tuned Responses
Example question: "What is SAP transaction FB01 used for?"
Pre‑trained GPT‑4o‑mini (typical behavior):
• Gives a vague answer like "FB01 is probably related to financial postings" and suggests checking SAP help.
• Lacks confidence and does not describe document types, debit/credit entries, or alternatives like FB50.
Fine‑tuned SAP Finance model:
• Explains that FB01 posts general accounting documents in FI, allowing manual entry of debit and credit line items for G/L, customer, or vendor accounts.
• Mentions that in S/4HANA there are more specific T‑codes (e.g., FB50 for pure G/L postings) but FB01 remains a generic posting transaction.
Example question: "How do I post a vendor invoice in SAP?"
Pre‑trained GPT‑4o‑mini:
• Returns a generic AP process description without naming T‑codes.
• Does not distinguish PO‑based vs non‑PO invoices.
Fine‑tuned SAP model:
• Points to FB60 for vendor invoices without a purchase order and MIRO for PO‑based invoices.
• References the 3‑way match (PO, goods receipt, invoice) and explains what data needs to be entered.
Comparison of Pre-Trained and Fine-Tuned Model Responses
Example Question: "What is SAP transaction FB01 used for?"
•	Pre-trained GPT-4o-mini Response:
Provides a vague statement, such as "FB01 is probably related to financial postings," and typically suggests consulting SAP help documentation.
•	Does not provide details regarding document types, the nature of debit or credit entries, or mention alternative transactions like FB50.

Fine-tuned SAP Finance Model Response:
•	Clearly explains that FB01 is used to post general accounting documents in Financial Accounting (FI).
•	Highlights the manual entry of debit and credit line items for general ledger (G/L), customer, or vendor accounts.
•	Notes that while S/4HANA provides more specific transaction codes (for example, FB50 for G/L postings), FB01 remains a generic transaction for posting documents.
Example Question: "How do I post a vendor invoice in SAP?"
•	Pre-trained GPT-4o-mini-Response:
•	Delivers a generic description of the accounts payable (AP) process.
•	Does not reference SAP transaction codes.
•	Fails to distinguish between purchase order (PO)-based and non-PO invoice postings.

Fine-tuned SAP Finance Model Response:
Specifically identifies FB60 as the transaction code for posting vendor invoices without a purchase order and MIRO for posting PO-based invoices.
References the three-way match process (purchase order, goods receipt, and invoice).
Explains the types of data required for entry during the invoice posting process.
Prompting Tips
• Keep questions focused on SAP finance; the model is optimized for this domain.
• Use SAP terminology directly (FB60, MIRO, cost center 1000, company code, etc.).
• Ask for the desired format, e.g., "Explain step‑by‑step" or "Answer briefly".
• Encourage the model to state assumptions when configuration is company‑specific.

Recommended Test Questions
Question	Expected Behavior
How do I post a vendor invoice in SAP?	Mentions FB60 or MIRO, explains 3-way match
What is cost center 1000?	Explains it as Administration/Overhead
Explain FB01 transaction	General document posting, debit/credit entries
What GL accounts are used for payroll?	References 6xxxxx series expense accounts

 
High-Impact Comparison Prompts: Pre-Trained vs Fine-Tuned Model
Prompt: "A goods receipt was posted but no accounting document was created. What could be wrong?"
Pre-trained	Fine-tuned
Gives a generic "check system settings" response.	Checks for missing valuation class in the material master, improper configuration of automatic account determination (OBYC) for BSX/WRX, differentiates between movement type 101 and 501, and whether the valuation area is active for the company code. Also suggests using OMJJ for movement type configuration.

Prompt: "Explain the document flow when I post MIRO for a PO-based invoice"
Pre-trained	Fine-tuned
Provides a basic explanation that the invoice is matched to the PO.	Describes the full process: ME21N creates the PO, MIGO (movement 101) posts the goods receipt and debits GR/IR clearing, MIRO matches the invoice, credits GR/IR clearing, and credits the vendor. Mentions RBKP/RSEG tables, document types RE, and the role of F.13/MR11 in handling residual GR/IR differences.
Others
Question/Topic	Pre-trained Model	Fine-tuned Model
Invoice matched to PO	Provides a basic explanation that the invoice is matched to the PO.	Describes the full process: ME21N creates the PO, MIGO (movement 101) posts the goods receipt and debits GR/IR clearing, MIRO matches the invoice, credits GR/IR clearing, and credits the vendor. Mentions RBKP/RSEG tables, document types RE, and the role of F.13/MR11 in handling residual GR/IR differences.
OBYC keys affecting goods receipt posting	Confused or generic	BSX, WRX, PRD, GBB with explanations
BAPI for posting vendor invoice programmatically	May not know	BAPI_INCOMINGINVOICE_CREATE, reference RBKP/RSEG structure
Difference between movement type 101 and 561	Guesses	101 = GR against PO (GR/IR clearing), 561 = initial stock entry (no PO, direct inventory)
OB52 control function	Doesn't know	Posting period open/close per company code, account type, period range
FAGL_FCV vs F.05	Confused	Both = foreign currency valuation. FAGL_FCV for New GL/S4, F.05 for classic GL

Key Points
For Technical Audiences
•	LoRA (Low-Rank Adaptation) enables efficient fine-tuning without full model retraining
•	JSONL chat completion format aligns with production API usage
•	Serverless deployment means no GPU quota management
•	Model can be accessed via same Azure OpenAI SDK/REST APIs
For Business Audiences
•	Reduce SAP consulting costs with AI-powered self-service
•	Accelerate finance team onboarding with intelligent assistance
•	Enterprise-grade security - data stays in your Azure tenant
•	Pay-as-you-go pricing starting at $1.70 per million tokens for training
Overall 
In summary, the fine-tuned model vastly outperforms the base model on SAP Finance queries – providing more accurate, specific, and useful answers with less prompting. This specialized performance comes at the cost of a small amount of training time and some hosting fees but delivers a high ROI when SAP expertise is needed from an AI assistant. The base model is only superior in areas unrelated to SAP (since it’s more general), but that’s not a concern for our use case where we want a focused expert. Fine-tuning has essentially transformed a generic model into an SAP finance specialist, highlighting the power of domain adaptation.
Best practices:
• Delete or scale down the deployment after demos to avoid idle hosting charges.
• Keep the fine‑tuned model artifact; redeploy it when needed instead of retraining.
• Monitor token usage and adjust capacity based on real traffic patterns.
Cost Estimate 
Fine-tuning and deploying a custom model incur additional costs on Azure. Here’s a breakdown (using GPT-4.0-mini as reference) and some guided management costs:
Component	Estimated Cost
Training (50 examples, 3 epochs)	~$0.50 - $2.00
Hosting (per hour when deployed)	~$1.70/hour
Inference (per 1M tokens)	Standard Azure OpenAI pricing
Note: Delete deployment after demo to avoid ongoing hosting charges. Inactive deployments are auto-deleted after 15 days. In essence, this demo showcased how Azure AI Foundry fine-tuning can bridge the gap between a generic AI model and a highly specialized enterprise assistant. By adapting the model to the SAP Finance domain, we unlocked its potential to serve a niche but valuable role. The methodology used here can be replicated for other modules (e.g., SAP SD, HR) or even other enterprise systems. It empowers organizations to create custom AI solutions tailored to their proprietary knowledge and processes, all while using Azure’s robust and scalable AI platform. We are now ready to deploy this solution within an enterprise setting. The Azure AI Foundry SAP Finance AI Assistant is live and ready to answer your team’s SAP questions!
Closing notes 
• Fine‑tuning GPT‑4o‑mini with LoRA in Azure AI Foundry creates a compact, cost‑efficient SAP Finance assistant.
• The fine‑tuned model dramatically outperforms the base model on SAP FI/CO questions, with minimal prompt engineering.
• VS Code is an effective environment for data preparation, testing, and automation.
• Integration with SAP Fiori and SAP BTP turns the model into a practical, embedded assistant for finance users.
• Costs are predictable and controllable; deleting the deployment when idle keeps the solution economical.
Files Included
6.	sap_finance_training.jsonl - 50 training examples
7.	sap_finance_validation.jsonl - 10 validation examples
8.	This demo guide document
Ready to demo Azure AI Foundry fine-tuning with SAP expertise!
Created by – 
aka.ms/amitlal

