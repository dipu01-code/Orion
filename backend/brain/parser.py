import re


CREATE_FOLDER_AND_OPEN_PATTERN = re.compile(
    r"^(?:open|launch|start)\s+(?:a\s+)?new\s+window\s+in\s+(?P<app>.+?)\s+"
    r"(?:and|then)\s+create\s+(?:a\s+)?folder\s+(?:named|called)\s+"
    r"(?P<folder>.+)$",
    re.IGNORECASE,
)

CREATE_FOLDER_PATTERN = re.compile(
    r"^create\s+(?:a\s+)?folder\s+(?:named|called)\s+(?P<folder>.+)$",
    re.IGNORECASE,
)

OPEN_NEW_WINDOW_PATTERN = re.compile(
    r"^(?:open|launch|start)\s+(?:a\s+)?new\s+window\s+in\s+(?P<app>.+)$",
    re.IGNORECASE,
)

OPEN_APPLICATION_PATTERN = re.compile(
    r"^(?:open|launch|start)\s+(?P<app>.+)$",
    re.IGNORECASE,
)

CALCULATOR_PATTERN = re.compile(
    r"^(?:what\s+is|calculate|compute)\s+(?P<expression>.+?)[?]?$",
    re.IGNORECASE,
)


def parse_command(command):
    command = command.strip()
    lowered_command = command.lower()

    if "system information" in lowered_command or "system info" in lowered_command:
        return {"intent": "system_info"}

    folder_workflow = CREATE_FOLDER_AND_OPEN_PATTERN.match(command)
    if folder_workflow:
        return {
            "intent": "create_folder_and_open_in_app",
            "app_name": _clean_value(folder_workflow.group("app")),
            "folder_name": _clean_folder_name(folder_workflow.group("folder")),
        }

    create_folder = CREATE_FOLDER_PATTERN.match(command)
    if create_folder:
        return {
            "intent": "create_folder",
            "folder_name": _clean_folder_name(create_folder.group("folder")),
        }

    new_window = OPEN_NEW_WINDOW_PATTERN.match(command)
    if new_window:
        return {
            "intent": "open_new_window",
            "app_name": _clean_value(new_window.group("app")),
        }

    calculator = CALCULATOR_PATTERN.match(command)
    if calculator:
        return {
            "intent": "calculate",
            "expression": _clean_expression(calculator.group("expression")),
        }

    open_application = OPEN_APPLICATION_PATTERN.match(command)
    if open_application:
        return {
            "intent": "open_application",
            "app_name": _clean_value(open_application.group("app")),
        }

    return {
        "intent": "unknown",
        "command": command,
    }


def _clean_folder_name(value):
    value = _clean_value(value)

    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1].strip()

    return value


def _clean_value(value):
    return value.strip().rstrip(".")


def _clean_expression(value):
    return (
        _clean_value(value)
        .replace("×", "*")
        .replace("x", "*")
        .replace("X", "*")
        .replace("÷", "/")
    )
