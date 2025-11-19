"""
Code Executor Module
Executes buggy Python code and captures source code and traceback.
"""
import sys
import traceback
from io import StringIO
from typing import Tuple, Optional


class CodeExecutor:
    """Executes Python code and captures execution results and errors."""
    
    def __init__(self):
        self.last_traceback = None
        self.last_stdout = None
        self.last_stderr = None
    
    def execute(self, code: str, code_filepath: Optional[str] = None) -> Tuple[bool, str, str]:
        """
        Execute Python code and capture the result.
        
        Args:
            code: The Python code to execute as a string
            code_filepath: Optional filepath for better traceback messages
            
        Returns:
            Tuple of (success: bool, stdout: str, error_info: str)
            - success: True if code executed without errors
            - stdout: Standard output from the execution
            - error_info: Error traceback if execution failed, empty string otherwise
        """
        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        
        success = True
        error_info = ""
        
        try:
            # Create a namespace for execution
            namespace = {
                '__name__': '__main__',
                '__file__': code_filepath or '<string>',
            }
            
            # Execute the code
            exec(code, namespace)
            
        except Exception as e:
            success = False
            # Capture the full traceback
            error_info = traceback.format_exc()
            self.last_traceback = error_info
            
        finally:
            # Get the captured output
            stdout_content = sys.stdout.getvalue()
            stderr_content = sys.stderr.getvalue()
            
            # Restore original stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
            self.last_stdout = stdout_content
            self.last_stderr = stderr_content
        
        return success, stdout_content, error_info
    
    def execute_file(self, filepath: str) -> Tuple[bool, str, str]:
        """
        Execute a Python file and capture the result.
        
        Args:
            filepath: Path to the Python file to execute
            
        Returns:
            Tuple of (success: bool, stdout: str, error_info: str)
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        return self.execute(code, filepath)
    
    def get_code_and_traceback(self, code: str, filepath: Optional[str] = None) -> Tuple[str, str]:
        """
        Execute code and return both the source code and traceback if there's an error.
        
        Args:
            code: The Python code to execute
            filepath: Optional filepath for the code
            
        Returns:
            Tuple of (source_code: str, traceback: str)
        """
        success, stdout, error_info = self.execute(code, filepath)
        
        if not success:
            return code, error_info
        else:
            return code, ""
