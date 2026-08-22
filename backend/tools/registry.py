from tools.system import get_system_info
from tools.applications import (
    open_application,
    open_new_window,
    open_folder_in_application
)
from tools.filesystem import create_folder


TOOLS = {
    "system_info": {
        "function": get_system_info,
        "description": "Get information about the current computer system."
    },

    "open_application": {
        "function": open_application,
        "description": "Open an application on the computer."
    },

    "open_new_window": {
        "function": open_new_window,
        "description": "Open a new window in an application."
    },

    "create_folder": {
        "function": create_folder,
        "description": "Create a folder on the computer."
    }
}


def run_tool(tool_name, *args, **kwargs):
    if tool_name not in TOOLS:
        return None

    return TOOLS[tool_name]["function"](*args, **kwargs)