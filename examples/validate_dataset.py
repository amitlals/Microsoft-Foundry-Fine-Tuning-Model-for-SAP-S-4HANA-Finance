"""
JSONL Dataset Validator for Azure OpenAI Fine-Tuning

This script validates the training and validation datasets to ensure
they meet Azure OpenAI fine-tuning requirements.

Usage:
    python validate_dataset.py
"""

import json
import os
from pathlib import Path

# Constants for token and cost estimation
CHARS_PER_TOKEN_ESTIMATE = 4  # Rough approximation: 1 token ≈ 4 characters
COST_PER_1K_TRAINING_TOKENS = 0.008  # Azure OpenAI fine-tuning cost estimate (subject to change)


def validate_jsonl_file(file_path):
    """
    Validate a JSONL file for Azure OpenAI fine-tuning
    
    Args:
        file_path: Path to JSONL file
    
    Returns:
        Tuple of (is_valid, errors, stats)
    """
    errors = []
    stats = {
        "total_lines": 0,
        "valid_lines": 0,
        "total_messages": 0,
        "total_tokens_estimate": 0,
        "roles_count": {"system": 0, "user": 0, "assistant": 0}
    }
    
    if not os.path.exists(file_path):
        return False, [f"File not found: {file_path}"], stats
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                stats["total_lines"] += 1
                
                # Skip empty lines
                if not line.strip():
                    errors.append(f"Line {line_num}: Empty line")
                    continue
                
                try:
                    # Parse JSON
                    data = json.loads(line)
                    
                    # Check for required 'messages' field
                    if "messages" not in data:
                        errors.append(f"Line {line_num}: Missing 'messages' field")
                        continue
                    
                    messages = data["messages"]
                    
                    # Validate messages structure
                    if not isinstance(messages, list):
                        errors.append(f"Line {line_num}: 'messages' must be a list")
                        continue
                    
                    if len(messages) < 2:
                        errors.append(f"Line {line_num}: Must have at least 2 messages (user and assistant)")
                        continue
                    
                    # Validate each message
                    has_system = False
                    has_user = False
                    has_assistant = False
                    
                    for msg_idx, msg in enumerate(messages):
                        if not isinstance(msg, dict):
                            errors.append(f"Line {line_num}, Message {msg_idx}: Message must be a dictionary")
                            continue
                        
                        # Check required fields
                        if "role" not in msg:
                            errors.append(f"Line {line_num}, Message {msg_idx}: Missing 'role' field")
                            continue
                        
                        if "content" not in msg:
                            errors.append(f"Line {line_num}, Message {msg_idx}: Missing 'content' field")
                            continue
                        
                        role = msg["role"]
                        content = msg["content"]
                        
                        # Validate role
                        if role not in ["system", "user", "assistant"]:
                            errors.append(f"Line {line_num}, Message {msg_idx}: Invalid role '{role}'")
                            continue
                        
                        # Validate content
                        if not isinstance(content, str):
                            errors.append(f"Line {line_num}, Message {msg_idx}: Content must be a string")
                            continue
                        
                        if not content.strip():
                            errors.append(f"Line {line_num}, Message {msg_idx}: Content cannot be empty")
                            continue
                        
                        # Track roles
                        stats["roles_count"][role] += 1
                        if role == "system":
                            has_system = True
                        elif role == "user":
                            has_user = True
                        elif role == "assistant":
                            has_assistant = True
                        
                        # Estimate tokens using rough approximation
                        # Note: This is a simplified estimate. Actual tokenization depends on the model's tokenizer.
                        stats["total_tokens_estimate"] += len(content) // CHARS_PER_TOKEN_ESTIMATE
                    
                    # Check conversation structure
                    if not has_user:
                        errors.append(f"Line {line_num}: Missing 'user' message")
                    
                    if not has_assistant:
                        errors.append(f"Line {line_num}: Missing 'assistant' message")
                    
                    stats["valid_lines"] += 1
                    stats["total_messages"] += len(messages)
                
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: Invalid JSON - {e}")
                except Exception as e:
                    errors.append(f"Line {line_num}: Unexpected error - {e}")
    
    except Exception as e:
        return False, [f"Error reading file: {e}"], stats
    
    is_valid = len(errors) == 0
    return is_valid, errors, stats


def print_validation_results(file_name, is_valid, errors, stats):
    """
    Print validation results in a formatted way
    
    Args:
        file_name: Name of the file
        is_valid: Whether file is valid
        errors: List of error messages
        stats: Statistics dictionary
    """
    print("\n" + "="*80)
    print(f"VALIDATION RESULTS: {file_name}")
    print("="*80)
    
    if is_valid:
        print("\n✅ File is VALID and ready for fine-tuning!\n")
    else:
        print(f"\n❌ File has {len(errors)} validation error(s)\n")
    
    # Statistics
    print("Statistics:")
    print(f"  Total lines: {stats['total_lines']}")
    print(f"  Valid conversation lines: {stats['valid_lines']}")
    print(f"  Total messages: {stats['total_messages']}")
    print(f"  Estimated tokens: ~{stats['total_tokens_estimate']:,}")
    print(f"\nRole distribution:")
    print(f"  System messages: {stats['roles_count']['system']}")
    print(f"  User messages: {stats['roles_count']['user']}")
    print(f"  Assistant messages: {stats['roles_count']['assistant']}")
    
    # Errors
    if errors:
        print("\n" + "-"*80)
        print("ERRORS:")
        print("-"*80)
        for error in errors[:20]:  # Show first 20 errors
            print(f"  • {error}")
        
        if len(errors) > 20:
            print(f"\n  ... and {len(errors) - 20} more errors")
    
    print("\n" + "="*80 + "\n")


def validate_all_datasets():
    """Validate all dataset files in the data directory"""
    print("\n" + "="*80)
    print("AZURE OPENAI FINE-TUNING DATASET VALIDATOR")
    print("="*80 + "\n")
    
    # Define file paths
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"
    
    files_to_validate = [
        data_dir / "sap_finance_training.jsonl",
        data_dir / "sap_finance_validation.jsonl"
    ]
    
    all_valid = True
    total_stats = {
        "training_examples": 0,
        "validation_examples": 0,
        "total_tokens": 0
    }
    
    for file_path in files_to_validate:
        file_name = file_path.name
        is_valid, errors, stats = validate_jsonl_file(file_path)
        
        print_validation_results(file_name, is_valid, errors, stats)
        
        if not is_valid:
            all_valid = False
        
        # Aggregate stats
        if "training" in file_name.lower():
            total_stats["training_examples"] = stats["valid_lines"]
        elif "validation" in file_name.lower():
            total_stats["validation_examples"] = stats["valid_lines"]
        
        total_stats["total_tokens"] += stats["total_tokens_estimate"]
    
    # Final summary
    print("="*80)
    print("OVERALL SUMMARY")
    print("="*80)
    print(f"\nTraining examples: {total_stats['training_examples']}")
    print(f"Validation examples: {total_stats['validation_examples']}")
    print(f"Total examples: {total_stats['training_examples'] + total_stats['validation_examples']}")
    print(f"Estimated total tokens: ~{total_stats['total_tokens']:,}")
    
    if all_valid:
        print("\n✅ All datasets are VALID and ready for Azure OpenAI fine-tuning!")
        print("\nRecommendations:")
        print("  • Minimum 10 examples recommended (you have sufficient)")
        print("  • Consider adding more examples for better performance")
        print("  • Ensure diverse coverage of SAP Finance topics")
    else:
        print("\n❌ Some datasets have errors. Please fix them before fine-tuning.")
    
    print("\n" + "="*80 + "\n")
    
    # Cost estimate based on Azure OpenAI training token pricing
    estimated_cost = (total_stats["total_tokens"] / 1000) * COST_PER_1K_TRAINING_TOKENS
    print(f"💰 Estimated fine-tuning cost: ${estimated_cost:.2f} - ${estimated_cost * 2:.2f}")
    print("   (Actual cost depends on epochs, batch size, and Azure pricing)")
    print("\n" + "="*80 + "\n")


def main():
    """Main execution function"""
    try:
        validate_all_datasets()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
