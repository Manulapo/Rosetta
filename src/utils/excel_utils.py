"""Excel file creation and management utilities."""

import os
from typing import List, Tuple, Dict
from collections import defaultdict
import pandas as pd

from ..core.analyzer import group_translations_by_prefix
from ..core.translator import translate_batch_with_openai
from .file_utils import ensure_directory_exists


def capitalize_first_letter(text: str) -> str:
    """
    Capitalize the first letter of the text while preserving the rest.
    
    Args:
        text: The text to capitalize
        
    Returns:
        Text with first letter capitalized
    """
    if not text or not isinstance(text, str):
        return text
    text = text.strip()
    if len(text) == 0:
        return text
    return text[0].upper() + text[1:] if len(text) > 1 else text.upper()


def create_excel_files_by_prefix(
    all_translations: List[Tuple[str, str]], 
    output_dir: str = ".", 
    use_ai_translation: bool = False
) -> List[Tuple[str, int]]:
    """
    Create separate Excel files for each key prefix (first part before the dot).
    
    Args:
        all_translations: List of (key, value) translation pairs
        output_dir: Directory to save Excel files
        use_ai_translation: Whether to use OpenAI for translations
        
    Returns:
        List of (filename, translation_count) tuples
    """
    # Group translations by prefix
    prefix_groups = group_translations_by_prefix(all_translations)
    created_files = []
    
    # Ensure output directory exists
    ensure_directory_exists(os.path.join(output_dir, "dummy.txt"))
    
    # Create Excel file for each prefix
    for prefix, translations in prefix_groups.items():
        print(f"\nCreating Excel file for prefix: '{prefix}' ({len(translations)} translations)")
        
        if use_ai_translation:
            # Use OpenAI to translate
            translated_data = translate_batch_with_openai(translations)
        else:
            # Create empty translations
            translated_data = []
            for key, value in sorted(translations.items()):
                translated_data.append({
                    'key': key,
                    'en': value,
                    'dk': '',  # Danish - empty
                    'sw': '',  # Swedish - empty  
                    'es': '',  # Spanish - empty
                    'pt': ''   # Portuguese - empty
                })
        
        df = pd.DataFrame(translated_data)
        
        # Create filename based on prefix
        filename = f"{prefix}_translations.xlsx"
        filepath = os.path.join(output_dir, filename)
        
        # Write to Excel
        df.to_excel(filepath, index=False, engine='openpyxl')
        created_files.append((filename, len(translations)))
        print(f"Created: {filename}")
    
    # Print summary
    print(f"\nExcel files created:")
    for filename, count in sorted(created_files):
        print(f"   -> {filename} - {count} translations")
    
    total_translations = sum(count for _, count in created_files)
    print(f"\nSummary:")
    print(f"   Total unique translations: {total_translations}")
    print(f"   Total files created: {len(created_files)}")
    
    if use_ai_translation:
        print(f"   OpenAI translations: Enabled")
    else:
        print(f"   AI translations: Disabled (empty columns)")
    
    return created_files


def create_single_excel_file(
    all_translations: List[Tuple[str, str]], 
    output_path: str = "translations.xlsx"
) -> None:
    """
    Create a single Excel file with all translations.
    
    Args:
        all_translations: List of (key, value) translation pairs
        output_path: Path for the output Excel file
    """
    # Create a dictionary to store unique key-value pairs
    unique_translations = {}
    for key, value in all_translations:
        if key not in unique_translations:
            unique_translations[key] = value
    
    # Create DataFrame
    df_data = []
    for key, value in sorted(unique_translations.items()):
        df_data.append({
            'key': key,
            'en': value,
            'da': '',  # Danish - empty
            'sw': '',  # Swedish - empty  
            'es': '',  # Spanish - empty
            'pt': ''   # Portuguese - empty
        })
    
    df = pd.DataFrame(df_data)
    
    # Ensure output directory exists
    ensure_directory_exists(output_path)
    
    # Write to Excel
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"\nSuccess: Excel file created: {output_path}")
    print(f"Total unique translations: {len(unique_translations)}")

def create_dictionary_from_excel(
    excel_path: str
) -> Dict[str, str]:
    """
    Create a dictionary from an Excel file containing translations.
    
    Args:
        excel_path: Path to the Excel file  
    Returns:
        Dictionary mapping keys to their English text
    """
    if not os.path.isfile(excel_path):
        print(f"Error: Excel file not found: {excel_path}")
        return {}
    
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return {}
    
    if 'key' not in df.columns or 'en' not in df.columns:
        print("Error: Excel file must contain 'key' and 'en' columns.")
        return {}
    
    translations_dict = {}
    for _, row in df.iterrows():
        key = str(row['key']).strip().lower()  # Convert key to lowercase
        value = str(row['en']).strip()
        if key and value:
            # Capitalize the first letter of the English text
            translations_dict[key] = capitalize_first_letter(value)

    return translations_dict    