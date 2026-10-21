"""Code Repository AST Context Packer and Pruner Engine.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional, Set
import ast
import re


class CodeRepositoryContextPacker:
    """Parses Python repository files using standard library AST, extracts imported symbols,
    prunes docstrings/comments to fit tight token budgets, and packs prioritized code context."""

    @classmethod
    def extract_file_symbols(cls, source_code: str) -> Dict[str, Any]:
        """Extracts top-level class names, function signatures, and imports using Python AST."""
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return {"imports": [], "classes": [], "functions": [], "syntax_valid": False}

        imports = []
        classes = []
        functions = []

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for alias in node.names:
                    imports.append(f"{mod}.{alias.name}")
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                    "line_number": node.lineno,
                })
            elif isinstance(node, ast.FunctionDef):
                args = [a.arg for a in node.args.args]
                functions.append({
                    "name": node.name,
                    "arguments": args,
                    "line_number": node.lineno,
                })

        return {
            "imports": imports,
            "classes": classes,
            "functions": functions,
            "syntax_valid": True,
        }

    @classmethod
    def prune_code_to_budget(
        cls,
        code: str,
        max_characters: int = 2000,
        strip_comments: bool = True,
        strip_docstrings: bool = True,
    ) -> Dict[str, Any]:
        """Compresses source code to fit within LLM context window token limits."""
        lines = code.splitlines()
        pruned_lines = []

        in_multiline_doc = False
        quote_char = None

        for line in lines:
            stripped = line.strip()

            if strip_comments and stripped.startswith("#"):
                continue

            if strip_docstrings:
                if not in_multiline_doc:
                    if stripped.startswith('"""') or stripped.startswith("'''"):
                        quote_char = stripped[:3]
                        if stripped.count(quote_char) >= 2 and len(stripped) > 3:
                            continue  # single-line docstring
                        in_multiline_doc = True
                        continue
                else:
                    if quote_char in stripped:
                        in_multiline_doc = False
                        quote_char = None
                    continue

            pruned_lines.append(line)

        compressed_code = "\n".join(pruned_lines)
        truncated = False
        if len(compressed_code) > max_characters:
            compressed_code = compressed_code[:max_characters] + "\n# ... [TRUNCATED DUE TO CONTEXT BUDGET]"
            truncated = True

        return {
            "original_length": len(code),
            "compressed_length": len(compressed_code),
            "compression_ratio": round(len(compressed_code) / max(1, len(code)), 2),
            "truncated": truncated,
            "packed_code": compressed_code,
        }

    @classmethod
    def pack_repository_context(
        cls,
        files: List[Dict[str, str]],
        focus_file: str,
        max_total_characters: int = 6000,
    ) -> Dict[str, Any]:
        """Packs multiple repository files prioritizing the focus file and directly imported sibling modules."""
        # Focus file gets highest budget allocation
        packed_files = []
        budget_remaining = max_total_characters

        # Order files: focus file first, then others
        ordered = sorted(files, key=lambda f: 0 if f.get("path") == focus_file else 1)

        for f in ordered:
            path = f.get("path", "file.py")
            raw_content = f.get("content", "")

            # Focus file gets up to 50% of budget; siblings get remaining budget
            file_budget = min(budget_remaining, max_total_characters // 2 if path == focus_file else budget_remaining)
            if file_budget <= 200:
                break

            pruned = cls.prune_code_to_budget(raw_content, max_characters=file_budget)
            symbols = cls.extract_file_symbols(raw_content)

            packed_files.append({
                "path": path,
                "is_focus": path == focus_file,
                "symbols_summary": f"Classes: {len(symbols['classes'])}, Functions: {len(symbols['functions'])}",
                "packed_content": pruned["packed_code"],
            })
            budget_remaining -= len(pruned["packed_code"])

        return {
            "focus_file": focus_file,
            "total_files_packed": len(packed_files),
            "budget_used": max_total_characters - budget_remaining,
            "packed_files": packed_files,
        }
