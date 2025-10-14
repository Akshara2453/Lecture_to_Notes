import os
import json

# -------------------------------
# Text File Utilities
# -------------------------------
def save_text_file(text, directory, filename):
    """
    Saves a string as a text file in the given directory.

    Args:
        text (str): Text content to save.
        directory (str): Directory path.
        filename (str): File name (with .txt extension).

    Returns:
        str: Full path to the saved file.
    """
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    return file_path


def read_text_file(file_path):
    """
    Reads a text file and returns its content.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: File content as a string.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# -------------------------------
# JSON Utilities
# -------------------------------
def save_json(file_path, data):
    """
    Saves a Python object as a JSON file.

    Args:
        file_path (str): Path to save JSON.
        data (dict/list): Python object to save.

    Returns:
        None
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_json(file_path):
    """
    Loads a JSON file and returns a Python object.

    Args:
        file_path (str): Path to JSON file.

    Returns:
        dict/list: Parsed JSON content, or empty dict if file not found.
    """
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
