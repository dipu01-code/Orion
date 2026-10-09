from tools.calculator import calculate
from tools.system import get_system_info
from tools.applications import (
    open_application,
    open_new_window,
    open_folder_in_application
)
from tools.filesystem import create_folder
from tools.inspection import git_status, inspect_project, read_file


TOOLS = {
    "system_info": {
        "function": get_system_info,
        "description": "Get information about the current computer system.",
        "parameters": {},
        "safety": "safe",
        "return_type": "dict",
    },

    "open_application": {
        "function": open_application,
        "description": "Open an application on the computer.",
        "parameters": {"app_name": "str"},
        "safety": "safe",
        "return_type": "tool_result",
    },

    "open_new_window": {
        "function": open_new_window,
        "description": "Open a new window in an application.",
        "parameters": {"app_name": "str"},
        "safety": "safe",
        "return_type": "tool_result",
    },

    "create_folder": {
        "function": create_folder,
        "description": "Create a folder on the computer.",
        "parameters": {"folder_name": "str", "location": "str | None"},
        "safety": "caution",
        "return_type": "tool_result",
    },

    "open_folder_in_application": {
        "function": open_folder_in_application,
        "description": "Open a folder in an application.",
        "parameters": {"app_name": "str", "folder_path": "str"},
        "safety": "safe",
        "return_type": "tool_result",
    },

    "calculate": {
        "function": calculate,
        "description": "Calculate a simple arithmetic expression.",
        "parameters": {"expression": "str"},
        "safety": "safe",
        "return_type": "tool_result",
    },
    "inspect_project": {
        "function": inspect_project,
        "description": "List files in a project without modifying it.",
        "parameters": {"directory": "str"}, "safety": "safe", "return_type": "tool_result",
    },
    "read_file": {
        "function": read_file,
        "description": "Read a UTF-8 text file without modifying it.",
        "parameters": {"path": "str"}, "safety": "safe", "return_type": "tool_result",
    },
    "git_status": {
        "function": git_status,
        "description": "Inspect read-only Git status in a directory.",
        "parameters": {"directory": "str"}, "safety": "safe", "return_type": "tool_result",
    },
}


def run_tool(tool_name, *args, **kwargs):
    if tool_name not in TOOLS:
        return {
            "success": False,
            "message": f"Unknown tool: {tool_name}",
        }

    return TOOLS[tool_name]["function"](*args, **kwargs)


def list_tools():
    return sorted(TOOLS.keys())


def describe_tool(tool_name):
    tool = TOOLS.get(tool_name)
    if not tool:
        return None

    return {
        key: value
        for key, value in tool.items()
        if key != "function"
    }


def model_tool_definitions():
    """Return provider-neutral function schemas without executable callables."""
    return tuple({
        "type": "function",
        "function": {
            "name": name,
            "description": tool["description"],
            "parameters": {
                "type": "object",
                "properties": {
                    parameter: {"type": "string"}
                    for parameter in tool["parameters"]
                },
                "required": list(tool["parameters"]),
            },
        },
    } for name, tool in TOOLS.items())
 
