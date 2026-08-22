from pathlib import Path


def create_folder(folder_name, location=None):

    if location:
        folder_path = Path(location).expanduser() / folder_name
    else:
        folder_path = Path.home() / folder_name

    try:
        folder_path.mkdir(parents=True, exist_ok=True)

        return {
            "success": True,
            "path": str(folder_path),
            "message": f"Folder created at {folder_path}"
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Could not create folder: {error}"
        }