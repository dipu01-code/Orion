from tools.registry import run_tool


class OrionBrain:

    def respond(self, command):
        original_command = command.strip()
        command = original_command.lower()

        if "hello" in command:
            return "Hello. I am ORION."

        elif "who are you" in command:
            return "I am ORION, your personal AI assistant."

        elif "status" in command:
            return "All systems are operational."

        elif "system information" in command or "system info" in command:
            info = run_tool("system_info")

            return (
                f"System: {info['system']}\n"
                f"Release: {info['release']}\n"
                f"Machine: {info['machine']}\n"
                f"Processor: {info['processor']}\n"
                f"Hostname: {info['hostname']}"
            )

        # Multi-action command: open window + create folder
        elif (
            "open a new window in " in command
            and "create a folder named " in command
        ):
            before_folder, folder_name = original_command.split(
                "create a folder named ", 1
            )

            folder_name = folder_name.strip()

            app_name = before_folder.lower().split(
                "open a new window in ", 1
            )[1].replace("and", "").strip()

            # Action 1: Open application window
            app_result = run_tool(
                "open_new_window",
                app_name
            )

            # Action 2: Create folder
            folder_result = run_tool(
                "create_folder",
                folder_name
            )

            return (
                f"{app_result}\n"
                f"{folder_result['message']}"
            )

        # Open a new window
        elif "open a new window in " in command:
            app_name = original_command.split(
                "open a new window in ", 1
            )[1].strip()

            return run_tool("open_new_window", app_name)

        # Open an application
        elif command.startswith("open "):
            app_name = original_command[5:].strip()

            if not app_name:
                return "Please tell me which application you want to open."

            return run_tool("open_application", app_name)

        else:
            return "I don't understand that command yet."