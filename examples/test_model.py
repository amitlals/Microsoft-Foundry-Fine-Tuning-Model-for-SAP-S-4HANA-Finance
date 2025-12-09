"""
SAP Finance Fine-Tuned Model Testing Script

This script demonstrates how to test the fine-tuned GPT-4o-mini model
for SAP S/4HANA Finance domain queries.

Prerequisites:
- Azure OpenAI resource deployed
- Fine-tuned model deployed
- Python 3.8+
- openai package installed: pip install openai

Usage:
    python test_model.py
"""

import os
from openai import AzureOpenAI

# Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "your-api-key-here")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "sap-finance-gpt4o-mini")
API_VERSION = "2024-08-01-preview"

# System prompt for SAP Finance expert
SYSTEM_PROMPT = "You are an expert SAP S/4HANA Finance consultant specializing in Financial Accounting (FI) and Controlling (CO) modules."

# Test queries covering various SAP Finance topics
TEST_QUERIES = [
    "What is transaction code FB50?",
    "Explain the difference between FB50 and F-02",
    "What is document splitting in SAP New G/L?",
    "How do I post a vendor invoice with transaction code FB60?",
    "What is FS00 used for?",
    "What are the key components of the SAP FI module?",
    "Explain cost center accounting in SAP CO",
    "How does the payment program F110 work?",
    "What is the purpose of profit center accounting?",
    "How do I configure automatic account determination for inventory postings?",
    "What is the difference between cost element and G/L account?",
    "How do I run month-end closing in SAP?",
    "What is the Universal Journal in S/4HANA?"
]


def initialize_client():
    """Initialize Azure OpenAI client"""
    try:
        client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        print("✅ Azure OpenAI client initialized successfully")
        return client
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return None


def test_single_query(client, query, verbose=True):
    """
    Test a single query against the fine-tuned model
    
    Args:
        client: Azure OpenAI client
        query: User query string
        verbose: Print detailed response
    
    Returns:
        Response text or None if error
    """
    try:
        if verbose:
            print(f"\n{'='*80}")
            print(f"Query: {query}")
            print(f"{'='*80}")
        
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=1000,
            top_p=0.95
        )
        
        answer = response.choices[0].message.content
        
        if verbose:
            print(f"\nResponse:\n{answer}")
            print(f"\n{'='*80}")
            print(f"Tokens used: {response.usage.total_tokens}")
            print(f"Completion tokens: {response.usage.completion_tokens}")
            print(f"{'='*80}\n")
        
        return answer
    
    except Exception as e:
        print(f"❌ Error testing query: {e}")
        return None


def run_test_suite(client):
    """
    Run comprehensive test suite against fine-tuned model
    
    Args:
        client: Azure OpenAI client
    """
    print("\n" + "="*80)
    print("SAP FINANCE FINE-TUNED MODEL TEST SUITE")
    print("="*80 + "\n")
    
    results = []
    total_tokens = 0
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n📝 Test {i}/{len(TEST_QUERIES)}")
        answer = test_single_query(client, query, verbose=False)
        
        if answer:
            results.append({
                "query": query,
                "answer": answer,
                "status": "✅ Success"
            })
            print(f"   ✅ Success: {query[:50]}...")
        else:
            results.append({
                "query": query,
                "answer": None,
                "status": "❌ Failed"
            })
            print(f"   ❌ Failed: {query[:50]}...")
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    successful = sum(1 for r in results if r["status"] == "✅ Success")
    print(f"\nTotal Tests: {len(TEST_QUERIES)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(TEST_QUERIES) - successful}")
    print(f"Success Rate: {(successful/len(TEST_QUERIES)*100):.1f}%")
    print("="*80 + "\n")


def interactive_mode(client):
    """
    Interactive testing mode - ask questions in real-time
    
    Args:
        client: Azure OpenAI client
    """
    print("\n" + "="*80)
    print("INTERACTIVE MODE - SAP Finance Assistant")
    print("="*80)
    print("\nAsk any SAP Finance question. Type 'quit' or 'exit' to end.\n")
    
    while True:
        try:
            query = input("You: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                continue
            
            print("\n🤖 Assistant: ", end="")
            answer = test_single_query(client, query, verbose=False)
            
            if answer:
                print(answer)
            else:
                print("Sorry, I encountered an error processing your request.")
            
            print("\n" + "-"*80 + "\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("SAP S/4HANA FINANCE - FINE-TUNED MODEL TESTING")
    print("="*80 + "\n")
    
    # Validate configuration
    if AZURE_OPENAI_API_KEY == "your-api-key-here":
        print("⚠️  Please set your Azure OpenAI API key in environment variables:")
        print("   export AZURE_OPENAI_API_KEY='your-actual-api-key'")
        print("   export AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com'")
        print("   export DEPLOYMENT_NAME='sap-finance-gpt4o-mini'")
        return
    
    # Initialize client
    client = initialize_client()
    if not client:
        return
    
    # Menu
    print("\nSelect testing mode:")
    print("1. Run automated test suite (13 predefined queries)")
    print("2. Interactive mode (ask your own questions)")
    print("3. Test single custom query")
    print("4. Exit")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            run_test_suite(client)
        elif choice == "2":
            interactive_mode(client)
        elif choice == "3":
            query = input("\nEnter your SAP Finance query: ").strip()
            if query:
                test_single_query(client, query, verbose=True)
        elif choice == "4":
            print("\n👋 Goodbye!")
        else:
            print("\n❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
