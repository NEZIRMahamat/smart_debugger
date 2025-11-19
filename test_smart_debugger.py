#!/usr/bin/env python
"""
Test script to validate Smart Debugger functionality without API key.
Tests the executor and patcher modules independently.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_debugger.executor import CodeExecutor
from smart_debugger.patcher import Patcher


def test_executor():
    """Test the CodeExecutor module."""
    print("Testing CodeExecutor...")
    executor = CodeExecutor()
    
    # Test 1: Valid code
    code = "print('Hello, World!')"
    success, stdout, error = executor.execute(code)
    assert success, "Valid code should execute successfully"
    assert "Hello, World!" in stdout, "Output should contain 'Hello, World!'"
    print("✓ Test 1 passed: Valid code execution")
    
    # Test 2: Syntax error
    code = "def test()\n    print('missing colon')"
    success, stdout, error = executor.execute(code)
    assert not success, "Invalid code should fail"
    assert len(error) > 0, "Error info should be captured"
    print("✓ Test 2 passed: Syntax error detection")
    
    # Test 3: Runtime error
    code = "x = 10 / 0"
    success, stdout, error = executor.execute(code)
    assert not success, "Code with runtime error should fail"
    assert "ZeroDivisionError" in error, "Error should contain ZeroDivisionError"
    print("✓ Test 3 passed: Runtime error detection")
    
    print("✓ All CodeExecutor tests passed!\n")


def test_patcher():
    """Test the Patcher module."""
    print("Testing Patcher...")
    patcher = Patcher()
    
    import tempfile
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        temp_file = f.name
        f.write("# Original code\nprint('test')")
    
    try:
        # Test 1: Apply patch
        original = "# Original code\nprint('test')"
        corrected = "# Corrected code\nprint('test fixed')"
        result = patcher.apply_patch(original, corrected, temp_file)
        assert result == corrected, "Patch should return corrected code"
        print("✓ Test 1 passed: Patch application")
        
        # Test 2: Verify backup
        backup_path = temp_file + ".backup"
        assert os.path.exists(backup_path), "Backup should exist"
        with open(backup_path, 'r') as f:
            backup_content = f.read()
        assert backup_content == original, "Backup should contain original code"
        print("✓ Test 2 passed: Backup creation")
        
        # Test 3: Restore backup
        restored = patcher.restore_backup(temp_file)
        assert restored, "Backup should be restored"
        with open(temp_file, 'r') as f:
            restored_content = f.read()
        assert restored_content == original, "Restored content should match original"
        print("✓ Test 3 passed: Backup restoration")
        
        # Test 4: Delete backup
        deleted = patcher.delete_backup(temp_file)
        assert deleted, "Backup should be deleted"
        assert not os.path.exists(backup_path), "Backup file should not exist"
        print("✓ Test 4 passed: Backup deletion")
        
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
        backup_path = temp_file + ".backup"
        if os.path.exists(backup_path):
            os.remove(backup_path)
    
    print("✓ All Patcher tests passed!\n")


def test_example_files():
    """Test that example files exist and contain expected errors."""
    print("Testing example files...")
    
    examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'examples')
    
    # Test example 1 (syntax error)
    example1 = os.path.join(examples_dir, 'buggy_example1.py')
    assert os.path.exists(example1), "Example 1 should exist"
    with open(example1, 'r') as f:
        content = f.read()
    assert "def calculate_sum(a, b)" in content, "Example 1 should have the buggy function"
    print("✓ Test 1 passed: Example 1 exists")
    
    # Test example 2 (runtime error)
    example2 = os.path.join(examples_dir, 'buggy_example2.py')
    assert os.path.exists(example2), "Example 2 should exist"
    with open(example2, 'r') as f:
        content = f.read()
    assert "divide_numbers" in content, "Example 2 should have divide_numbers function"
    print("✓ Test 2 passed: Example 2 exists")
    
    # Test example 3 (type error)
    example3 = os.path.join(examples_dir, 'buggy_example3.py')
    assert os.path.exists(example3), "Example 3 should exist"
    with open(example3, 'r') as f:
        content = f.read()
    assert "greet_user" in content, "Example 3 should have greet_user function"
    print("✓ Test 3 passed: Example 3 exists")
    
    print("✓ All example file tests passed!\n")


def main():
    """Run all tests."""
    print("=" * 70)
    print("Smart Debugger - Test Suite")
    print("=" * 70)
    print()
    
    try:
        test_executor()
        test_patcher()
        test_example_files()
        
        print("=" * 70)
        print("✓ All tests passed successfully!")
        print("=" * 70)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
