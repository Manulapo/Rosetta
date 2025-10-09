#!/usr/bin/env python3
"""
Rosetta - Translation scanning and management CLI tool.

A tool for scanning Vue.js, JavaScript, and TypeScript files for translation
instances and managing conflicts, redundancy, and automated translations.
"""

import sys
from src.cli import main

if __name__ == "__main__":
    sys.exit(main())