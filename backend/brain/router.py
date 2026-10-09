from brain.planner import build_plan
from tools.registry import run_tool


def route_intent(intent):
    intent_name = intent["intent"]

    if intent_name == "system_info":
        return _format_system_info(run_tool("system_info"))

    if intent_name == "create_folder_and_open_in_app":
        return _create_folder_and_open_in_app(
            intent["app_name"],
            intent["folder_name"],
        )

    if intent_name == "create_folder":
        return _format_tool_result(run_tool("create_folder", intent["folder_name"]))

    if intent_name == "calculate":
        return _format_tool_result(run_tool("calculate", intent["expression"]))

    if intent_name == "open_new_window":
        result = run_tool("open_new_window", intent["app_name"])
        return _format_tool_result(result)

    if intent_name == "open_application":
        if not intent["app_name"]:
            return "Please tell me which application you want to open."

        result = run_tool("open_application", intent["app_name"])
        return _format_tool_result(result)

    return "I don't understand that command yet."


def _create_folder_and_open_in_app(app_name, folder_name):
    plan = build_plan({
        "intent": "create_folder_and_open_in_app",
        "app_name": app_name,
        "folder_name": folder_name,
    })
    results = _execute_plan(plan)
    folder_result = results["folder"]

    if not folder_result["success"]:
        return folder_result["message"]

    app_result = results["application"]

    if not app_result["success"]:
        return (
            f"{folder_result['message']}\n"
            f"{app_result['message']}"
        )

    return (
        f"{folder_result['message']}\n"
        f"{app_result['message']}"
    )


def _format_system_info(info):
    return (
        f"System: {info['system']}\n"
        f"Release: {info['release']}\n"
        f"Machine: {info['machine']}\n"
        f"Processor: {info['processor']}\n"
        f"Hostname: {info['hostname']}"
    )


def _format_tool_result(result):
    if isinstance(result, dict) and "message" in result:
        return result["message"]

    return result


def _execute_plan(plan):
    results = {}

    for step in plan:
        args = [_resolve_arg(arg, results) for arg in step.get("args", [])]
        result = run_tool(step["tool"], *args)
        results[step["save_as"]] = result

        if isinstance(result, dict) and result.get("success") is False:
            break

    return results


def _resolve_arg(arg, results):
    if isinstance(arg, dict) and "from" in arg and "field" in arg:
        return results[arg["from"]][arg["field"]]

    return arg
