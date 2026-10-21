# genpark-code-repository-ast-context-packer-and-pruner-skill

Token-budget-aware repository context extractor, import graph crawler, and symbol-dense code prompt packer.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Python AST Symbol Harvester**: Parses code via standard library AST to extract imports, class methods, and function signatures.
- **Context Token Budget Pruner**: Compresses code files by stripping comments and docstrings while preserving indentation and executable syntax.
- **Priority-Weighted Repository Context Packer**: Maximizes LLM prompt density by dedicating budget to active focus files and directly related dependencies.

## Architecture

```
[Repository Files + Focus File Target + Token Budget]
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│             CodeRepositoryContextPacker             │
│  - Python AST Symbol & Signature Extractor          │
│  - Comment & Docstring Space Compressor             │
│  - Dynamic Context Budget Allocation Matrix         │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
[Optimized, High-Density Packed Repository Context]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `extract_file_symbols`: Extracts imports, classes, and function signatures from Python source using AST.
- `pack_repository_context`: Packs multiple repository files within an LLM context token/character budget prioritizing focus files.

## Quickstart (Python API)

```python
from client import CodeRepositoryContextPacker

code = "import os\ndef test(): return True"
symbols = CodeRepositoryContextPacker.extract_file_symbols(code)
print("Symbols:", symbols["functions"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
