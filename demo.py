#!/usr/bin/env python
"""
Demo script showing how to use Smart Debugger.

This script demonstrates the Smart Debugger's capabilities without requiring
a GROQ API key by testing individual components.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from smart_debugger import CodeExecutor, Patcher


def demo_executor():
    """Demonstrate the Code Executor component."""
    print("=" * 70)
    print("DEMO 1: Code Executor Component")
    print("=" * 70)
    print("\nThe Code Executor runs Python code and captures errors.\n")
    
    executor = CodeExecutor()
    
    # Example 1: Valid code
    print("Example 1: Running valid code")
    print("-" * 70)
    code = """
for i in range(3):
    print(f"Hello, iteration {i}!")
"""
    print("Code to execute:")
    print(code)
    
    success, stdout, error = executor.execute(code)
    print(f"\nExecution successful: {success}")
    print(f"Output:\n{stdout}")
    
    # Example 2: Code with error
    print("\n" + "=" * 70)
    print("Example 2: Running code with a division by zero error")
    print("-" * 70)
    code = """
def divide(a, b):
    return a / b

result = divide(10, 0)
print(f"Result: {result}")
"""
    print("Code to execute:")
    print(code)
    
    success, stdout, error = executor.execute(code)
    print(f"\nExecution successful: {success}")
    print(f"Error captured:\n{error}")


def demo_patcher():
    """Demonstrate the Patcher component."""
    print("\n" + "=" * 70)
    print("DEMO 2: Patcher Component")
    print("=" * 70)
    print("\nThe Patcher applies fixes and manages backups.\n")
    
    import tempfile
    patcher = Patcher()
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        temp_file = f.name
        original_code = """# Original buggy code
x = 10 / 0  # This will cause an error
print(x)
"""
        f.write(original_code)
    
    print("Original code:")
    print(original_code)
    
    # Apply a patch
    corrected_code = """# Corrected code
x = 10 / 2  # Fixed: changed 0 to 2
print(x)
"""
    patcher.apply_patch(original_code, corrected_code, temp_file)
    
    print("\nCorrected code:")
    print(corrected_code)
    
    print(f"✓ Patch applied to {temp_file}")
    print(f"✓ Backup created at {temp_file}.backup")
    
    # Read the patched file
    with open(temp_file, 'r') as f:
        content = f.read()
    print(f"\nFile content after patching:\n{content}")
    
    # Cleanup
    os.remove(temp_file)
    if os.path.exists(temp_file + ".backup"):
        os.remove(temp_file + ".backup")


def demo_full_flow():
    """Demonstrate the full debugging flow concept."""
    print("\n" + "=" * 70)
    print("DEMO 3: Full Smart Debugger Flow (Conceptual)")
    print("=" * 70)
    print("\nThis is how the Smart Debugger works with GROQ API:\n")
    
    print("1. CODE EXECUTOR: Run the buggy code and capture the error")
    print("   Input: Python code")
    print("   Output: Traceback and error message")
    print()
    
    print("2. LLM ANALYZER: Send code + error to GROQ API")
    print("   Input: Source code + traceback")
    print("   Output: Corrected code from AI")
    print()
    
    print("3. PATCHER: Apply the AI's correction")
    print("   Input: Corrected code")
    print("   Output: Fixed file (with backup)")
    print()
    
    print("4. LOOP: Repeat steps 1-3 until code runs without errors")
    print("   - Maximum 5 iterations by default")
    print("   - Prevents infinite loops")
    print()
    
    print("Example usage with GROQ API key:")
    print("-" * 70)
    print("""
from smart_debugger import SmartDebugger

# Initialize with your GROQ API key
debugger = SmartDebugger(api_key="your-groq-api-key")

# Debug a file
success, fixed_code, history = debugger.debug_file("buggy_script.py")

if success:
    print("✓ Code fixed successfully!")
    print(fixed_code)
""")


def demo_examples():
    """Show the example files."""
    print("\n" + "=" * 70)
    print("DEMO 4: Example Buggy Files")
    print("=" * 70)
    print("\nThe repository includes three example files:\n")
    
    examples = [
        ("examples/buggy_example1.py", "Syntax Error (missing colon)"),
        ("examples/buggy_example2.py", "Runtime Error (division by zero)"),
        ("examples/buggy_example3.py", "Type Error (string + integer)"),
    ]
    
    for filepath, description in examples:
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        if os.path.exists(full_path):
            print(f"File: {filepath}")
            print(f"Error Type: {description}")
            print("-" * 70)
            with open(full_path, 'r') as f:
                print(f.read())
            print()


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("SMART DEBUGGER - Interactive Demo")
    print("=" * 70)
    print("\nThis demo shows how the Smart Debugger works.")
    print("Note: Full AI debugging requires a GROQ API key.\n")
    
    try:
        demo_executor()
        demo_patcher()
        demo_full_flow()
        demo_examples()
        
        print("=" * 70)
        print("✓ Demo completed successfully!")
        print("=" * 70)
        print("\nTo use Smart Debugger with GROQ API:")
        print("1. Get a free API key from https://console.groq.com/")
        print("2. Set environment variable: export GROQ_API_KEY='your-key'")
        print("3. Run: python -m smart_debugger.main examples/buggy_example1.py")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Demo error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
