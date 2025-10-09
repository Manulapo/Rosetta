#!/usr/bin/env python3
"""
Rosetta - Translation scanning and management CLI tool.

DEPRECATED: This file is kept for backward compatibility.
Please use the new modular structure with `python main.py` or the individual modules.

The functionality has been reorganized into:
- src/config/settings.py - Configuration and settings
- src/core/scanner.py - File scanning functionality  
- src/core/analyzer.py - Translation analysis and conflict detection
- src/core/translator.py - OpenAI translation functionality
- src/utils/excel_utils.py - Excel file creation
- src/utils/file_utils.py - File utilities
- src/cli/commands.py - Command-line interface

To use the new structure:
    python main.py [folder] [options]

Or import individual modules:
    from src.cli import main
    from src.core import scan_folder
    etc.
"""

import sys
import warnings

# Issue deprecation warning
warnings.warn(
    "rosetta.py is deprecated. Please use 'python main.py' or import from the src/ modules.",
    DeprecationWarning,
    stacklevel=2
)

# Import the new CLI for backward compatibility
try:
    from src.cli import main
except ImportError:
    print("Error: Could not import the new modular structure.")
    print("Please ensure the src/ directory and modules are properly installed.")
    sys.exit(1)

if __name__ == "__main__":
    # Run the new CLI for backward compatibility
    sys.exit(main())