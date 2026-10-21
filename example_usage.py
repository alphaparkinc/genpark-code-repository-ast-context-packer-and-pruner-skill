"""Example usage for Code Repository AST Context Packer & Pruner."""
from client import CodeRepositoryContextPacker

if __name__ == "__main__":
    sample_code = '''
"""Module docstring explaining complex architecture."""
import os
import sys

# Calculation helper
def compute_metrics(x: int, y: int) -> int:
    """Computes basic sum."""
    return x + y

class DataPipeline:
    """Manages stream execution."""
    def run(self):
        return True
'''

    # Test 1: Symbol Extraction
    symbols = CodeRepositoryContextPacker.extract_file_symbols(sample_code)
    print("Extracted Imports:", symbols["imports"])
    print("Extracted Functions:", [f["name"] for f in symbols["functions"]])
    print("Extracted Classes:", [c["name"] for c in symbols["classes"]])

    # Test 2: Compression & Packing
    files = [
        {"path": "pipeline.py", "content": sample_code},
        {"path": "utils.py", "content": "# Utility functions\ndef helper(): return 42"},
    ]
    packed = CodeRepositoryContextPacker.pack_repository_context(files, focus_file="pipeline.py", max_total_characters=800)
    print(f"\nPacked {packed['total_files_packed']} files, budget used: {packed['budget_used']} chars.")
