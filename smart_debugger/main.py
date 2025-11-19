"""
Smart Debugger - AI-powered Python code debugger using GROQ API

Main module that orchestrates the debugging process:
1. Execute buggy code and capture errors
2. Analyze errors using LLM
3. Apply fixes
4. Repeat until no errors (with loop prevention)
"""
import os
import sys
from typing import Optional, Tuple
from .executor import CodeExecutor
from .analyzer import LLMAnalyzer
from .patcher import Patcher


class SmartDebugger:
    """Main debugger that orchestrates the debugging process."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.1-70b-versatile", max_iterations: int = 5):
        """
        Initialize the Smart Debugger.
        
        Args:
            api_key: GROQ API key (if None, will use GROQ_API_KEY env variable)
            model: The GROQ model to use for analysis
            max_iterations: Maximum number of debugging iterations to prevent infinite loops
        """
        self.executor = CodeExecutor()
        self.analyzer = LLMAnalyzer(api_key=api_key, model=model)
        self.patcher = Patcher()
        self.max_iterations = max_iterations
        self.debug_history = []
    
    def debug_code(self, code: str, filepath: Optional[str] = None, verbose: bool = True) -> Tuple[bool, str, list]:
        """
        Debug the given code until it executes without errors.
        
        Args:
            code: The Python code to debug
            filepath: Optional filepath for the code (used for better error messages)
            verbose: Whether to print progress information
            
        Returns:
            Tuple of (success: bool, final_code: str, history: list)
            - success: True if code was successfully debugged
            - final_code: The final corrected code
            - history: List of debugging iterations with details
        """
        current_code = code
        iteration = 0
        
        if verbose:
            print("=" * 70)
            print("Smart Debugger - Starting debugging process")
            print("=" * 70)
        
        while iteration < self.max_iterations:
            iteration += 1
            
            if verbose:
                print(f"\n--- Iteration {iteration}/{self.max_iterations} ---")
            
            # Step 1: Execute the code
            success, stdout, error_info = self.executor.execute(current_code, filepath)
            
            if success:
                # Code executed successfully!
                if verbose:
                    print("✓ Code executed successfully!")
                    if stdout:
                        print("\nOutput:")
                        print(stdout)
                
                self.debug_history.append({
                    'iteration': iteration,
                    'status': 'success',
                    'code': current_code,
                    'output': stdout
                })
                
                # Apply the final corrected code if filepath is provided
                if filepath:
                    self.patcher.apply_patch(code, current_code, filepath)
                
                return True, current_code, self.debug_history
            
            # Step 2: There was an error, analyze it with LLM
            if verbose:
                print("✗ Error detected:")
                print(error_info)
                print("\nAnalyzing error with LLM...")
            
            try:
                corrected_code = self.analyzer.analyze_error(current_code, error_info)
                
                if verbose:
                    print("✓ LLM analysis complete. Correction suggested.")
                
                self.debug_history.append({
                    'iteration': iteration,
                    'status': 'error',
                    'code': current_code,
                    'error': error_info,
                    'corrected_code': corrected_code
                })
                
                # Step 3: Apply the patch
                current_code = corrected_code
                
            except Exception as e:
                if verbose:
                    print(f"✗ Error during LLM analysis: {str(e)}")
                
                self.debug_history.append({
                    'iteration': iteration,
                    'status': 'llm_error',
                    'code': current_code,
                    'error': error_info,
                    'llm_error': str(e)
                })
                
                return False, current_code, self.debug_history
        
        # Max iterations reached without success
        if verbose:
            print(f"\n✗ Max iterations ({self.max_iterations}) reached without resolving all errors.")
        
        return False, current_code, self.debug_history
    
    def debug_file(self, filepath: str, verbose: bool = True) -> Tuple[bool, str, list]:
        """
        Debug a Python file.
        
        Args:
            filepath: Path to the Python file to debug
            verbose: Whether to print progress information
            
        Returns:
            Tuple of (success: bool, final_code: str, history: list)
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        return self.debug_code(code, filepath, verbose)


def main():
    """Main entry point for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Smart Debugger - AI-powered Python code debugger')
    parser.add_argument('file', help='Python file to debug')
    parser.add_argument('--api-key', help='GROQ API key (or use GROQ_API_KEY env variable)')
    parser.add_argument('--model', default='llama-3.1-70b-versatile', help='GROQ model to use')
    parser.add_argument('--max-iterations', type=int, default=5, help='Maximum debugging iterations')
    parser.add_argument('--quiet', action='store_true', help='Suppress progress output')
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = args.api_key or os.getenv('GROQ_API_KEY')
    if not api_key:
        print("Error: GROQ API key not provided. Use --api-key or set GROQ_API_KEY environment variable.")
        sys.exit(1)
    
    # Create debugger and run
    debugger = SmartDebugger(api_key=api_key, model=args.model, max_iterations=args.max_iterations)
    success, final_code, history = debugger.debug_file(args.file, verbose=not args.quiet)
    
    if success:
        print("\n" + "=" * 70)
        print("Debugging completed successfully!")
        print("=" * 70)
        sys.exit(0)
    else:
        print("\n" + "=" * 70)
        print("Debugging failed.")
        print("=" * 70)
        sys.exit(1)


if __name__ == '__main__':
    main()
