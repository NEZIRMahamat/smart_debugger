"""
Patcher Module
Applies corrections to buggy code.
"""
import os
from typing import Optional


class Patcher:
    """Applies corrections to buggy code files."""
    
    def __init__(self):
        self.backup_enabled = True
    
    def apply_patch(self, original_code: str, corrected_code: str, filepath: Optional[str] = None) -> str:
        """
        Apply the corrected code.
        
        Args:
            original_code: The original buggy code
            corrected_code: The corrected code from LLM
            filepath: Optional filepath to save the corrected code
            
        Returns:
            The corrected code that was applied
        """
        if filepath:
            # Create backup of original file if it exists
            if os.path.exists(filepath) and self.backup_enabled:
                backup_path = f"{filepath}.backup"
                with open(filepath, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
            
            # Write the corrected code
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(corrected_code)
        
        return corrected_code
    
    def restore_backup(self, filepath: str) -> bool:
        """
        Restore a file from its backup.
        
        Args:
            filepath: The filepath to restore
            
        Returns:
            True if backup was restored, False if no backup exists
        """
        backup_path = f"{filepath}.backup"
        
        if os.path.exists(backup_path):
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            
            return True
        
        return False
    
    def delete_backup(self, filepath: str) -> bool:
        """
        Delete the backup file.
        
        Args:
            filepath: The original filepath
            
        Returns:
            True if backup was deleted, False if no backup exists
        """
        backup_path = f"{filepath}.backup"
        
        if os.path.exists(backup_path):
            os.remove(backup_path)
            return True
        
        return False
