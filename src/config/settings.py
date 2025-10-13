"""Configuration settings for Rosetta CLI."""

import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Translation regex pattern
# Matches t('key', 'value') or $t("key", "value") 
# Also handles $t('key', 'value', {params}) with optional third parameter
# Very strict: no newlines in key or value parts
TRANSLATION_REGEX = re.compile(
    r"""(?:\$t|t)\(\s*(['"])((?:\\.|[^'"\n])*?)\1\s*,\s*(['"])((?:\\.|[^'"\n])*?)\3\s*(?:,\s*\{[^}]*?\})?\s*\)""",
)

# File scanning configuration
DEFAULT_EXTENSIONS = (".vue", ".js", ".ts")

# Language mapping for translations
LANGUAGE_CODES = {
    'DK': 'Danish',
    'SW': 'Swedish', 
    'es': 'Spanish',
    'pt': 'Portuguese'
}

DEFAULT_TARGET_LANGUAGES = ['DK', 'SW', 'es', 'pt']

# OpenAI Translation configuration
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.3
OPENAI_MAX_TOKENS = 200

# Rate limiting
TRANSLATIONS_PER_BATCH = 10
DELAY_BETWEEN_BATCHES = 1  # seconds