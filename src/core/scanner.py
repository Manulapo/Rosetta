"""File scanning functionality for extracting translations."""

import os
from typing import List, Tuple, Dict

from ..config import TRANSLATION_REGEX, DEFAULT_EXTENSIONS


def extract_translations_from_file(filepath: str) -> Tuple[List[Tuple[str, str]], List[str]]:
    """
    Extract translation instances from a single file.
    
    Args:
        filepath: Path to the file to scan
        
    Returns:
        Tuple of (translations_list, errors_list)
        translations_list: List of (key, value) tuples
        errors_list: List of error messages
    """
    translations = []
    errors = []
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            for match in TRANSLATION_REGEX.finditer(content):
                key, value = match.group(2), match.group(4)
                if key and value:
                    translations.append((key, value))
                else:
                    errors.append(match.group(0))
    except Exception as e:
        errors.append(f"File read error: {e}")
    
    return translations, errors


def scan_folder(
    folder: str, 
    extensions: Tuple[str, ...] = DEFAULT_EXTENSIONS, 
    show_log: bool = False
) -> Tuple[List[Tuple[str, str]], Dict[str, int], List[str]]:
    """
    Scan a folder or single file recursively for translation instances.
    
    Args:
        folder: Root folder to scan OR path to a single file
        extensions: File extensions to include in scan
        show_log: Whether to print detailed scanning logs
        
    Returns:
        Tuple of (all_translations, file_counts, errors)
        all_translations: List of all (key, value) translation pairs found
        file_counts: Dictionary mapping file paths to number of translations found
        errors: List of error messages encountered
    """
    all_translations = []
    errors = []
    file_counts = {}

    # Check if input is a file or directory
    if os.path.isfile(folder):
        # Single file mode
        if folder.endswith(extensions):
            print(f"📄 Scanning file: {folder}")
            translations, file_errors = extract_translations_from_file(folder)
            file_counts[folder] = len(translations)
            
            if show_log:
                print(f"🔍 Checking {folder} → {len(translations)} instance(s) found")

            all_translations.extend(translations)
            errors.extend([f"{folder}: {err}" for err in file_errors])
        else:
            print(f"⚠️  File {folder} does not match extensions: {extensions}")
    else:
        # Directory mode (original behavior)
        print(f"📁 Scanning folder: {folder} for files with extensions: {extensions}")

        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(extensions):
                    path = os.path.join(root, file)
                    translations, file_errors = extract_translations_from_file(path)
                    file_counts[path] = len(translations)
                    
                    if show_log:
                        print(f"🔍 Checking {path} → {len(translations)} instance(s) found")

                    all_translations.extend(translations)
                    errors.extend([f"{path}: {err}" for err in file_errors])

    return all_translations, file_counts, errors