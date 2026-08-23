import subprocess
import shutil


APP_ALIASES = {
    "vs code": "Visual Studio Code",
    "vscode": "Visual Studio Code",
    "code": "Visual Studio Code",
}


def is_vs_code(app_name):
    return normalize_app_name(app_name) == "Visual Studio Code"


def open_folder_in_application(app_name, folder_path):
    app_name = normalize_app_name(app_name)

    try:
        if is_vs_code(app_name):
            code_command = shutil.which("code")

            if code_command:
                subprocess.run(
                    [code_command, "-n", folder_path],
                    check=True
                )
                return _success(f"Opened {folder_path} in {app_name}.")

            subprocess.run(
                ["open", "-na", app_name, "--args", "-n", folder_path],
                check=True
            )
            return _success(f"Opened {folder_path} in {app_name}.")

        subprocess.run(
            ["open", "-na", app_name, folder_path],
            check=True
        )

        return _success(f"Opened {folder_path} in {app_name}.")

    except subprocess.CalledProcessError:
        return _failure(f"I could not open {folder_path} in {app_name}.")


def normalize_app_name(app_name):
    return APP_ALIASES.get(app_name.lower(), app_name)


def open_application(app_name):
    app_name = normalize_app_name(app_name)

    try:
        subprocess.run(
            ["open", "-a", app_name],
            check=True
        )

        return _success(f"Opening {app_name}.")

    except subprocess.CalledProcessError:
        return _failure(f"I could not open {app_name}. It may not be installed.")


def open_new_window(app_name):
    app_name = normalize_app_name(app_name)

    try:
        if is_vs_code(app_name):
            code_command = shutil.which("code")

            if code_command:
                subprocess.run(
                    [code_command, "-n"],
                    check=True
                )
                return _success(f"Opening a new window in {app_name}.")

            subprocess.run(
                ["open", "-na", app_name, "--args", "-n"],
                check=True
            )
            return _success(f"Opening a new window in {app_name}.")

        subprocess.run(
            ["open", "-na", app_name],
            check=True
        )

        return _success(f"Opening a new window in {app_name}.")

    except subprocess.CalledProcessError:
        return _failure(f"I could not open a new window in {app_name}.")


def _success(message):
    return {
        "success": True,
        "message": message,
    }


def _failure(message):
    return {
        "success": False,
        "message": message,
    }
