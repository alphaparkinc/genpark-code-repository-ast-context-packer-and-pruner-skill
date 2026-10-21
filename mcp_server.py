"""MCP server for Code Repository AST Context Packer & Pruner."""
import sys
import json
from client import CodeRepositoryContextPacker


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "extract_file_symbols",
                    "description": "Extracts imports, classes, and function signatures from Python source using AST",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "source_code": {"type": "string"},
                        },
                        "required": ["source_code"],
                    },
                },
                {
                    "name": "pack_repository_context",
                    "description": "Packs multiple repository files within an LLM context token/character budget prioritizing focus files",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "files": {
                                "type": "array",
                                "description": "Array of files with 'path' and 'content'",
                            },
                            "focus_file": {"type": "string"},
                            "max_total_characters": {"type": "integer", "default": 6000},
                        },
                        "required": ["files", "focus_file"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "extract_file_symbols":
            res = CodeRepositoryContextPacker.extract_file_symbols(args.get("source_code", ""))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "pack_repository_context":
            res = CodeRepositoryContextPacker.pack_repository_context(
                args.get("files", []),
                args.get("focus_file", ""),
                max_total_characters=args.get("max_total_characters", 6000),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
