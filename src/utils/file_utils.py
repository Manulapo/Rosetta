"""File utility functions."""

import os
from typing import List, Tuple


def get_file_list(folder: str, extensions: Tuple[str, ...]) -> List[str]:
    """
    Get list of files with specified extensions in a folder.
    
    Args:
        folder: Root folder to search
        extensions: File extensions to include
        
    Returns:
        List of file paths
    """
    file_list = []
    
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(extensions):
                file_list.append(os.path.join(root, file))
    
    return file_list


def ensure_directory_exists(file_path: str) -> None:
    """
    Ensure the directory for a file path exists.
    
    Args:
        file_path: Full path to a file
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)