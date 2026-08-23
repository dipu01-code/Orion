def build_plan(intent):
    intent_name = intent["intent"]

    if intent_name == "create_folder_and_open_in_app":
        return [
            {
                "tool": "create_folder",
                "args": [intent["folder_name"]],
                "save_as": "folder",
            },
            {
                "tool": "open_folder_in_application",
                "args": [
                    intent["app_name"],
                    {"from": "folder", "field": "path"},
                ],
                "save_as": "application",
            },
        ]

    return []
