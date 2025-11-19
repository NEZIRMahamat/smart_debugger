"""
LLM Analyzer Module
Uses GROQ API to analyze source code and traceback to suggest fixes.
"""
import os
from typing import Optional
from groq import Groq


class LLMAnalyzer:
    """Analyzes code errors using GROQ LLM API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.1-70b-versatile"):
        """
        Initialize the LLM analyzer.
        
        Args:
            api_key: GROQ API key (if None, will use GROQ_API_KEY env variable)
            model: The GROQ model to use for analysis
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ API key must be provided or set in GROQ_API_KEY environment variable")
        
        self.model = model
        self.client = Groq(api_key=self.api_key)
    
    def analyze_error(self, source_code: str, traceback: str) -> str:
        """
        Analyze the error and provide a fixed version of the code.
        
        Args:
            source_code: The buggy source code
            traceback: The error traceback from execution
            
        Returns:
            The corrected code as a string
        """
        prompt = self._build_analysis_prompt(source_code, traceback)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert Python debugging assistant. "
                            "When given buggy code and its error traceback, you analyze the issue "
                            "and provide a corrected version of the code. "
                            "Return ONLY the corrected Python code without any explanations, "
                            "markdown formatting, or code blocks. "
                            "The code should be ready to execute directly."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=2000,
            )
            
            corrected_code = response.choices[0].message.content.strip()
            
            # Clean up any markdown code blocks if present
            corrected_code = self._clean_code_response(corrected_code)
            
            return corrected_code
            
        except Exception as e:
            raise RuntimeError(f"Error calling GROQ API: {str(e)}")
    
    def _build_analysis_prompt(self, source_code: str, traceback: str) -> str:
        """Build the prompt for the LLM."""
        return f"""Here is a buggy Python code and its error traceback:

BUGGY CODE:
```python
{source_code}
```

ERROR TRACEBACK:
```
{traceback}
```

Please analyze this error and provide the corrected Python code. Return ONLY the corrected code, without any explanations or markdown formatting."""
    
    def _clean_code_response(self, response: str) -> str:
        """
        Clean the LLM response to extract only the Python code.
        
        Args:
            response: The raw response from the LLM
            
        Returns:
            Cleaned Python code
        """
        # Remove markdown code blocks if present
        lines = response.split('\n')
        cleaned_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```python'):
                in_code_block = True
                continue
            elif line.strip().startswith('```'):
                in_code_block = False
                continue
            elif in_code_block or not any(line.strip().startswith(marker) for marker in ['```']):
                cleaned_lines.append(line)
        
        # If we found code blocks, return the cleaned content
        if cleaned_lines and cleaned_lines != lines:
            return '\n'.join(cleaned_lines)
        
        # Otherwise, return the original response (already clean)
        return response
