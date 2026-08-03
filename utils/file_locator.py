import os

# Project root is always one level above this file (utils/), regardless of
# which directory a notebook or script is run from.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_path(folder_name, file_name):
    """
    Returns the full path of a specified file from a given folder.

    Parameters:
        folder_name (str): Name of the folder containing the file.
        file_name (str): Name of the file to load from the folder.

    Returns:
        str: Full path to the file from a given folder,
             Create a folder with same name, if not exist.

    Example:
        >>> create_path('images', 'logo.png')
        '/path/to/project/images/logo.png'
    """
    folder_path = os.path.join(PROJECT_ROOT, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)

    return file_path
