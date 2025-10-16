"""Command-line interface commands and argument parsing."""

import argparse
import sys
import os
import time
import pandas as pd
from datetime import datetime
from typing import List, Optional, Dict

from ..core import (
    scan_folder,
    generate_report,
    check_openai_api_key,
)
from ..utils import create_excel_files_by_prefix
from ..utils.excel_utils import create_dictionary_from_excel, capitalize_first_letter
from ..utils.file_utils import ensure_directory_exists
from ..core.translator import translate_batch_with_openai, translate_with_openai
from ..config import DEFAULT_EXTENSIONS, DEFAULT_TARGET_LANGUAGES, TRANSLATIONS_PER_BATCH, DELAY_BETWEEN_BATCHES


def get_default_output_dir() -> str:
    """
    Get the default output directory with timestamp.
    
    Returns:
        Path to default output directory: output/output-DD-MM-YYYY_HH-MM
    """
    today = datetime.now()
    timestamp = today.strftime("%d-%m-%Y_%H-%M")
    return os.path.join("output", f"output-{timestamp}")


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser with subcommands.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Rosetta - Translation management tool for multi-language applications",
        prog="rosetta"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # SCAN command - for analyzing code folders
    scan_parser = subparsers.add_parser('scan', help='Scan code folder for translations')
    scan_parser.add_argument('folder', help='Path to the folder to scan')
    scan_parser.add_argument(
        '--extensions',
        nargs='+',
        default=list(DEFAULT_EXTENSIONS),
        help=f'File extensions to scan (default: {" ".join(DEFAULT_EXTENSIONS)})'
    )
    scan_parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview mode - show analysis without creating files'
    )
    scan_parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for generated files (default: output/output-DD-MM-YYYY_HH-MM)"
    )
    scan_parser.add_argument(
        "--show-log",
        action="store_true",
        help="Show detailed processing logs"
    )
    
    # Scan output options (mutually exclusive)
    scan_output = scan_parser.add_mutually_exclusive_group()
    scan_output.add_argument(
        '--excel',
        action='store_true',
        help='Create Excel files for translation (empty columns)'
    )
    scan_output.add_argument(
        '--translate',
        action='store_true',
        help='Create Excel files with AI translations (requires OPENAI_API_KEY)'
    )
    
    # TRANSLATE command - for translating existing Excel files
    translate_parser = subparsers.add_parser('translate', help='Translate an existing Excel file with AI')
    translate_parser.add_argument('file', help='Path to Excel file to translate')
    translate_parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for generated files (default: output/output-DD-MM-YYYY_HH-MM)"
    )
    
    return parser


def validate_openai_setup(use_translation: bool) -> bool:
    """
    Validate OpenAI setup if translation is requested.
    
    Args:
        use_translation: Whether translation was requested
        
    Returns:
        True if setup is valid or not needed, False otherwise
    """
    if use_translation:
        is_ready, status_msg = check_openai_api_key()
        print(status_msg)
        if not is_ready:
            print("Cannot proceed with translation. Please set your OPENAI_API_KEY environment variable.")
            return False
    return True


def run_scan_command(
    folder: str,
    show_log: bool = False,
    create_excel: bool = False,
    use_translation: bool = False,
    preview_mode: bool = False,
    extensions: tuple = DEFAULT_EXTENSIONS,
    output_dir: str = None
) -> int:
    """
    Execute the main scan command.
    
    Args:
        folder: Folder to scan
        show_log: Whether to show detailed logs
        create_excel: Whether to create Excel files
        use_translation: Whether to use OpenAI translation
        preview_mode: Whether to show preview
        extensions: File extensions to scan
        output_dir: Output directory for files
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Use default output directory if none provided
    if output_dir is None:
        output_dir = get_default_output_dir()
    
    # Validate OpenAI setup if needed
    if not validate_openai_setup(use_translation):
        return 1
    
    try:
        # Scan the folder
        all_translations, file_counts, errors = scan_folder(
            folder, 
            extensions=tuple(extensions), 
            show_log=show_log
        )
        
        # Generate analysis report
        report_data = generate_report(
            all_translations, 
            file_counts, 
            errors, 
            preview_mode=preview_mode
        )
        
        # Create Excel files if requested and not in preview mode
        if create_excel and not preview_mode:
            has_issues = (
                len(report_data.get('errors', [])) > 0 or
                len(report_data.get('conflicts', {})) > 0 or
                len(report_data.get('exact_redundancy', {})) > 0 or
                len(report_data.get('pattern_redundancy', {})) > 0
            )
            
            if has_issues and use_translation:
                print("\nISSUES DETECTED:")
                print("   Found the following issues in translations:")
                if len(report_data.get('conflicts', {})) > 0:
                    print(f"   - {len(report_data.get('conflicts', {}))} key conflicts found")
                if len(report_data.get('exact_redundancy', {})) > 0:
                    print(f"   - {len(report_data.get('exact_redundancy', {}))} exact redundancies found")
                if len(report_data.get('pattern_redundancy', {})) > 0:
                    print(f"   - {len(report_data.get('pattern_redundancy', {}))} pattern redundancies found")
                if len(report_data.get('errors', [])) > 0:
                    print(f"   - {len(report_data.get('errors', []))} scanning errors found")
                
                print("\n   These issues may affect translation quality.")
                while True:
                    try:
                        response = input("\nContinue anyway? (y/n): ").strip().lower()
                        if response in ['', 'y', 'yes']:
                            print("Proceeding with AI translation...")
                            create_excel_files_by_prefix(
                                all_translations, 
                                output_dir=output_dir,
                                use_ai_translation=True
                            )
                            break
                        elif response in ['n', 'no']:
                            print("Process Stopped by user.")
                            break
                        else:
                            print("Please enter 'Y' for yes or 'N' for no.")
                    except KeyboardInterrupt:
                        print("\nCancelled. Creating Excel files without AI translation...")
                        create_excel_files_by_prefix(
                            all_translations, 
                            output_dir=output_dir,
                            use_ai_translation=False
                        )
                        break
            elif has_issues:
                print("\nFound issues in translations. Creating Excel files without AI translation...")
                print("Please review and fix conflicts/redundancies manually.")
                
                create_excel_files_by_prefix(
                    all_translations, 
                    output_dir=output_dir,
                    use_ai_translation=False
                )
            else:
                create_excel_files_by_prefix(
                    all_translations, 
                    output_dir=output_dir,
                    use_ai_translation=use_translation
                )
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


def translate_batch_with_capitalization(
    translations_dict: Dict[str, str], 
    target_languages: List[str] = None
) -> List[Dict[str, str]]:
    """
    Translate all English texts to target languages using OpenAI with capitalized results.
    
    Args:
        translations_dict: Dictionary mapping keys to English text
        target_languages: List of target language codes
        
    Returns:
        List of dictionaries containing capitalized translations for each language
    """
    if target_languages is None:
        target_languages = DEFAULT_TARGET_LANGUAGES.copy()
        
    translated_data = []
    total_translations = len(translations_dict)
    
    # Token usage tracking
    total_tokens = 0
    total_prompt_tokens = 0
    total_completion_tokens = 0
    
    print(f"\nStarting OpenAI translation of {total_translations} texts to {len(target_languages)} languages...")
    print("This may take a few minutes...")
    
    for i, (key, english_text) in enumerate(translations_dict.items(), 1):
        print(f"Translating {i}/{total_translations}: '{key[:50]}{'...' if len(key) > 50 else ''}'")
        
        # Ensure English text is capitalized and key is lowercase
        capitalized_english = capitalize_first_letter(english_text)
        lowercase_key = key.lower()
        
        row_data = {
            'key': lowercase_key,
            'en': capitalized_english
        }
        
        # Translate to each target language
        for lang in target_languages:
            print(f"  -> {lang}...", end=' ')
            translation, token_usage = translate_with_openai(capitalized_english, lang)
            
            # Track token usage if available
            if token_usage:
                total_tokens += token_usage.total_tokens
                total_prompt_tokens += token_usage.prompt_tokens
                total_completion_tokens += token_usage.completion_tokens
            
            # Capitalize the translation result
            row_data[lang] = capitalize_first_letter(translation)
            print("Done")
        
        translated_data.append(row_data)
        
        # Small delay to avoid rate limiting
        if i % TRANSLATIONS_PER_BATCH == 0:
            print(f"  (Completed {i}/{total_translations} translations)")
            time.sleep(DELAY_BETWEEN_BATCHES)
    
    print(f"\nOpenAI translation complete! Processed {total_translations} texts")
    print(f"Token usage summary:")
    print(f"  Total tokens used: {total_tokens:,}")
    print(f"  Prompt tokens: {total_prompt_tokens:,}")
    print(f"  Completion tokens: {total_completion_tokens:,}")
    if total_translations > 0 and len(target_languages) > 0:
        avg_tokens = total_tokens // (total_translations * len(target_languages))
        print(f"  Average tokens per translation: {avg_tokens}")
    
    return translated_data


def run_translate_from_excel_command(
    excel_path: str,
    output_dir: str = None
) -> int:
    """
    Execute translation directly from an Excel file.
    
    Args:
        excel_path: Path to the Excel file to translate
        output_dir: Output directory for the translated file
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Use default output directory if none provided
    if output_dir is None:
        output_dir = get_default_output_dir()
    
    # Validate OpenAI setup
    if not validate_openai_setup(True):
        return 1
    
    try:
        # Check if file exists and is Excel
        if not os.path.isfile(excel_path):
            print(f"Error: File not found: {excel_path}")
            return 1
            
        if not excel_path.lower().endswith(('.xlsx', '.xls')):
            print(f"Error: File must be an Excel file (.xlsx or .xls): {excel_path}")
            return 1
        
        print(f"Reading Excel file: {excel_path}")
        
        # Read translations from Excel file
        translations_dict = create_dictionary_from_excel(excel_path)
        
        if not translations_dict:
            print("Error: No valid translations found in Excel file.")
            print("Make sure the file contains 'key' and 'en' columns with data.")
            return 1
        
        print(f"Found {len(translations_dict)} translations to process")
        
        # Translate using OpenAI with capitalization
        translated_data = translate_batch_with_capitalization(translations_dict)
        
        # Save the translated data to a new Excel file
        ensure_directory_exists(os.path.join(output_dir, "dummy.txt"))
        
        # Create output filename
        base_name = os.path.splitext(os.path.basename(excel_path))[0]
        output_filename = f"{base_name}_translated.xlsx"
        output_filepath = os.path.join(output_dir, output_filename)
        
        # Save to Excel
        df = pd.DataFrame(translated_data)
        df.to_excel(output_filepath, index=False, engine='openpyxl')
        
        print(f"\nTranslation complete!")
        print(f"Input file: {excel_path}")
        print(f"Output file: {output_filepath}")
        print(f"Translations processed: {len(translations_dict)}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


def main(args: Optional[List[str]] = None) -> int:
    """
    Main CLI entry point.
    
    Args:
        args: Optional list of command line arguments
        
    Returns:
        Exit code
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    # If no command specified, show help
    if not parsed_args.command:
        parser.print_help()
        return 1
    
    # Set default output directory if not provided
    if not parsed_args.output_dir:
        parsed_args.output_dir = get_default_output_dir()
    
    # Handle scan command
    if parsed_args.command == 'scan':
        # Validate OpenAI setup if translation is requested
        if parsed_args.translate and not validate_openai_setup(True):
            return 1
        
        return run_scan_command(
            folder=parsed_args.folder,
            show_log=parsed_args.show_log,
            create_excel=parsed_args.excel or parsed_args.translate,
            use_translation=parsed_args.translate,
            preview_mode=parsed_args.preview,
            extensions=tuple(parsed_args.extensions),
            output_dir=parsed_args.output_dir
        )
    
    # Handle translate command
    elif parsed_args.command == 'translate':
        # Always validate OpenAI setup for translate command
        if not validate_openai_setup(True):
            return 1
        
        return run_translate_from_excel_command(
            excel_path=parsed_args.file,
            output_dir=parsed_args.output_dir
        )
    
    # This shouldn't happen, but just in case
    parser.print_help()
    return 1