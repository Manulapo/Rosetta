"""Core modules initialization."""

from .scanner import extract_translations_from_file, scan_folder
from .analyzer import (
    normalize_dynamic_value,
    analyze_translations,
    group_translations_by_prefix,
    print_preview,
    generate_report,
)
from .translator import (
    check_openai_api_key,
    translate_with_openai,
    translate_batch_with_openai,
)

__all__ = [
    "extract_translations_from_file",
    "scan_folder",
    "normalize_dynamic_value",
    "analyze_translations", 
    "group_translations_by_prefix",
    "print_preview",
    "generate_report",
    "check_openai_api_key",
    "translate_with_openai",
    "translate_batch_with_openai",
]