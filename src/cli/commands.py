"""Command-line interface commands and argument parsing."""

import argparse
import sys
import os
from datetime import datetime
from typing import List, Optional

from ..core import (
    scan_folder,
    generate_report,
    check_openai_api_key,
)
from ..utils import create_excel_files_by_prefix
from ..config import DEFAULT_EXTENSIONS


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
    Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Rosetta - Scan folder or file for translation instances and analyze conflicts",
        prog="rosetta"
    )
    
    parser.add_argument(
        "folder", 
        help="Folder path to scan for translation files OR path to a single file"
    )
    
    parser.add_argument(
        "--log", 
        action="store_true", 
        help="Show detailed file scanning logs"
    )
    
    parser.add_argument(
        "--excel", 
        action="store_true", 
        help="Create Excel files with translations organized by prefix"
    )
    
    parser.add_argument(
        "--translate", 
        action="store_true", 
        help="Use OpenAI to fill translations in other languages (requires OPENAI_API_KEY)"
    )
    
    parser.add_argument(
        "--preview", 
        action="store_true", 
        help="Show all translation dictionaries grouped by prefix"
    )
    
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=DEFAULT_EXTENSIONS,
        help=f"File extensions to scan (default: {' '.join(DEFAULT_EXTENSIONS)})"
    )
    
    parser.add_argument(
        "--output-dir",
        default=get_default_output_dir(),
        help="Output directory for Excel files (default: output/output-DD-MM-YYYY-HH-MM)"
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
    
    return run_scan_command(
        folder=parsed_args.folder,
        show_log=parsed_args.log,
        create_excel=parsed_args.excel,
        use_translation=parsed_args.translate,
        preview_mode=parsed_args.preview,
        extensions=parsed_args.extensions,
        output_dir=parsed_args.output_dir
    )