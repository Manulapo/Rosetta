"""Centralized message templates for Rosetta CLI."""


class MSG:
    """Message templates with emoji formatting for consistent output."""
    
    # === DYNAMIC MESSAGE BUILDERS ===
    @staticmethod
    def success(text: str) -> str:
        """Format a success message."""
        return f"✅ {text}"
    
    @staticmethod
    def error(text: str) -> str:
        """Format an error message."""
        return f"❌ Error: {text}"
    
    @staticmethod
    def info(text: str) -> str:
        """Format an info message."""
        return f"ℹ️  {text}"
    
    @staticmethod
    def warning(text: str) -> str:
        """Format a warning message."""
        return f"⚠️  {text}"
    
    # === SUCCESS MESSAGES ===
    FILE_CREATED = "✅ Created: {filename}"
    TRANSLATION_COMPLETE = "✅ Translation complete!"
    OPENAI_TRANSLATION_COMPLETE = "✅ OpenAI translation complete! Processed {count} texts"
    API_KEY_VALID = "✅ OpenAI API key is valid and ready"
    PROCEEDING_WITH_TRANSLATION = "✅ Proceeding with AI translation..."
    
    # === ERROR MESSAGES ===
    FILE_NOT_FOUND = "❌ Error: File not found: {path}"
    INVALID_EXCEL_FILE = "❌ Error: File must be an Excel file (.xlsx or .xls): {path}"
    NO_TRANSLATIONS_FOUND = "❌ Error: No valid translations found in Excel file."
    EXCEL_READ_ERROR = "❌ Error reading Excel file: {error}"
    EXCEL_MISSING_COLUMNS = "❌ Error: Excel file must contain 'key' and 'en' columns."
    CANNOT_PROCEED_TRANSLATION = "❌ Cannot proceed with translation. Please set your OPENAI_API_KEY environment variable."
    API_KEY_NOT_FOUND = "❌ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
    API_KEY_INVALID = "❌ OpenAI API key error: {error}"
    API_KEY_PLACEHOLDER = "⚠️  Please replace 'your-api-key-here' with your actual OpenAI API key in the script"
    FILE_EXTENSION_MISMATCH = "⚠️  File {path} does not match extensions: {extensions}"
    
    # === INFO MESSAGES ===
    SCANNING_FILE = "📄 Scanning file: {path}"
    SCANNING_FOLDER = "📁 Scanning folder: {folder} for files with extensions: {extensions}"
    READING_EXCEL = "📖 Reading Excel file: {path}"
    CREATING_EXCEL_PREFIX = "📝 Creating Excel file for prefix: '{prefix}' ({count} translations)"
    CHECKING_FILE = "🔍 Checking {path} → {count} instance(s) found"
    FOUND_TRANSLATIONS = "📊 Found {count} translations to process"
    
    # === PROGRESS MESSAGES ===
    TRANSLATING_ITEM = "📝 Translating {current}/{total}: '{key}'"
    TRANSLATING_TO_LANG = "  → {lang}..."
    TRANSLATION_DONE = "✓"
    BATCH_PAUSE = "  ⏸️  (Completed {current}/{total} translations)"
    STARTING_TRANSLATION = "🌐 Starting OpenAI translation of {count} texts to {langs} languages..."
    TRANSLATION_TIME_WARNING = "⏳ This may take a few minutes..."
    
    # === HEADERS ===
    HEADER_REPORT = "\n=== 📊 ROSETTA SCAN REPORT 📊 ==="
    HEADER_SUMMARY = "\n📋 SUMMARY:"
    HEADER_TOKEN_USAGE = "\n📊 Token usage summary:"
    HEADER_CONFLICTS = "\n⚠️  KEY CONFLICTS:"
    HEADER_EXACT_REDUNDANCY = "\n🔄 EXACT REDUNDANCIES:"
    HEADER_PATTERN_REDUNDANCY = "\n🔄 PATTERN REDUNDANCIES:"
    HEADER_ERRORS = "\n❌ ERRORS:"
    HEADER_PREVIEW = "\n=== 🔍 PREVIEW: All Translation Dictionaries ==="
    HEADER_PREVIEW_END = "\n=== ✅ END PREVIEW ==="
    HEADER_EXCEL_CREATED = "\n📊 Excel files created:"
    HEADER_FINAL_SUMMARY = "\n📋 Summary:"
    HEADER_ISSUES_DETECTED = "\n⚠️  ISSUES DETECTED:"
    
    # === SUMMARY MESSAGES ===
    SUMMARY_FILES_SCANNED = "- Files scanned: {count}"
    SUMMARY_TOTAL_INSTANCES = "- Total instances: {count}"
    SUMMARY_KEY_CONFLICTS = "- Key conflicts: {count}"
    SUMMARY_EXACT_REDUNDANCIES = "- Exact redundancies: {count}"
    SUMMARY_PATTERN_REDUNDANCIES = "- Pattern redundancies: {count}"
    SUMMARY_ERRORS = "- Errors: {count}"
    SUMMARY_UNIQUE_TRANSLATIONS = "📊 Total unique translations found: {count}"
    SUMMARY_PREFIX_GROUPS = "📁 Number of prefix groups: {count}"
    SUMMARY_TOTAL_UNIQUE = "   • Total unique translations: {count}"
    SUMMARY_FILES_CREATED = "   • Total files created: {count}"
    SUMMARY_OPENAI_ENABLED = "   • OpenAI translations: ✅ Enabled"
    SUMMARY_AI_DISABLED = "   • AI translations: ⚠️  Disabled (empty columns)"
    
    # === TOKEN USAGE ===
    TOKEN_TOTAL = "  • Total tokens used: {count:,}"
    TOKEN_PROMPT = "  • Prompt tokens: {count:,}"
    TOKEN_COMPLETION = "  • Completion tokens: {count:,}"
    TOKEN_AVERAGE = "  • Average tokens per translation: {count}"
    
    # === HINTS ===
    HINT_EXCEL_COLUMNS = "💡 Make sure the file contains 'key' and 'en' columns with data."
    HINT_FIX_CONFLICTS = "📝 Please review and fix conflicts/redundancies manually."
    
    # === USER PROMPTS ===
    PROMPT_CONTINUE = "\n❓ Continue anyway? (y/n): "
    PROMPT_INVALID_RESPONSE = "⚠️  Please enter 'Y' for yes or 'N' for no."
    
    # === STATUS MESSAGES ===
    PROCESS_STOPPED = "🛑 Process stopped by user."
    CANCELLED_NO_TRANSLATION = "\n⚠️  Cancelled. Creating Excel files without AI translation..."
    ISSUES_FOUND_NO_TRANSLATION = "\n⚠️  Found issues in translations. Creating Excel files without AI translation..."
    ISSUES_AFFECT_QUALITY = "\n   ⚡ These issues may affect translation quality."
    ISSUES_FOUND_DETAIL = "   Found the following issues in translations:"
    
    # === ISSUE DETAILS ===
    ISSUE_CONFLICTS = "   • {count} key conflicts found"
    ISSUE_EXACT_REDUNDANCY = "   • {count} exact redundancies found"
    ISSUE_PATTERN_REDUNDANCY = "   • {count} pattern redundancies found"
    ISSUE_SCANNING_ERRORS = "   • {count} scanning errors found"
    
    # === OUTPUT FILES ===
    OUTPUT_INPUT_FILE = "📥 Input file: {path}"
    OUTPUT_OUTPUT_FILE = "📤 Output file: {path}"
    OUTPUT_TRANSLATIONS_PROCESSED = "📊 Translations processed: {count}"
    OUTPUT_EXCEL_FILE = "✅ Success: Excel file created: {path}"
    OUTPUT_FILE_LIST_ITEM = "   • {filename} - {count} translations"
    
    # === PREFIX GROUPS ===
    PREFIX_GROUP_HEADER = "\n--- 📂 {prefix} ({count} translations) ---"
    PREFIX_TRANSLATION_ITEM = "  '{key}': '{value}'"
