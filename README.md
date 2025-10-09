# Rosetta CLI

A powerful CLI tool for scanning and managing translations in Vue.js, JavaScript, and TypeScript files. Rosetta helps you find translation instances, detect conflicts and redundancy, and automatically generate translations using OpenAI.

## Features

- **File Scanning**: Recursively scan Vue.js, JavaScript, and TypeScript files for translation instances
- **Conflict Detection**: Find same keys with different values
- **Redundancy Analysis**: Identify duplicate translations and similar patterns
- **Excel Export**: Generate organized Excel files with translations grouped by prefix
- **AI Translation**: Automatic translation to multiple languages using OpenAI GPT
- **Preview Mode**: View all translations organized by category before exporting
- **Detailed Reports**: Comprehensive analysis of translation issues and statistics

## Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key (for AI translation features)

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh
```

### Option 2: Manual Setup

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Set OpenAI API Key (Optional)

For AI translation features, you need to set your OpenAI API key:

**Option 1: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

**Option 2: Using .env file**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# OPENAI_API_KEY=your-openai-api-key-here
```

**Get your API key from:** https://platform.openai.com/account/api-keys

#### 3. Run Basic Scan

```bash
# Scan a project folder
python main.py /path/to/your/project

# Or scan a single file
python main.py /path/to/your/file.vue
```

## Usage

### Basic Commands

```bash
# Scan a project folder
python main.py /path/to/project

# Scan a single file
python main.py /path/to/component.vue

# Scan with detailed logs
python main.py /path/to/project --log

# Create Excel files without AI translation
python main.py /path/to/project --excel

# Create Excel files with AI translation
python main.py /path/to/project --excel --translate

# Preview translations without creating files
python main.py /path/to/project --preview
```

### Command Options

| Option | Description |
|--------|-------------|
| `folder` | **Required.** Path to the folder to scan OR path to a single file |
| `--log` | Show detailed file scanning logs |
| `--excel` | Create Excel files with translations organized by prefix |
| `--translate` | Use OpenAI to fill translations in other languages |
| `--preview` | Show all translation dictionaries grouped by prefix |
| `--extensions` | File extensions to scan (default: .vue .js .ts) |
| `--output-dir` | Output directory for Excel files (default: output/output-DD-MM-YYYY_HH:MM) |

### Advanced Examples

```bash
# Scan a single file with detailed logs
python main.py ./components/UserProfile.vue --log

# Scan specific file types only
python main.py /path/to/project --extensions .vue .jsx

# Output Excel files to specific directory
python main.py /path/to/project --excel --output-dir ./custom-translations

# Full analysis with AI translation and detailed logs (uses default timestamped output)
python main.py /path/to/project --log --excel --translate
```

## Translation Patterns

The tool automatically detects these translation patterns:

```javascript
// Vue.js / JavaScript patterns
t('key', 'value')
$t("key", "value")
$t('key', 'value', {params})

// Examples
t('welcome', 'Welcome to our app')
$t("user.name", "User Name")
$t('notification.count', 'You have {count} notifications', {count: 5})
```

## Supported Languages

Currently supports automatic translation to:

- 🇩🇰 **Danish (DK)**
- 🇸🇪 **Swedish (SW)**
- 🇪🇸 **Spanish (ES)**
- 🇵🇹 **Portuguese (PG)**

*Languages can be configured in `src/config/settings.py`*

## Project Structure

```
rosetta-cli/
├── 📄 main.py                    # Main entry point
├── 📄 rosetta.py                 # Deprecated (backward compatibility)
├── 📂 src/
│   ├── 📄 __init__.py
│   ├── 📂 cli/
│   │   ├── 📄 __init__.py
│   │   └── 📄 commands.py        # CLI commands and argument parsing
│   ├── 📂 core/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 scanner.py         # File scanning functionality
│   │   ├── 📄 analyzer.py        # Translation analysis and conflict detection
│   │   └── 📄 translator.py      # OpenAI translation functionality
│   ├── 📂 utils/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 file_utils.py      # File utilities
│   │   └── 📄 excel_utils.py     # Excel file creation
│   └── 📂 config/
│       ├── 📄 __init__.py
│       └── 📄 settings.py        # Configuration and settings
├── 📂 tests/                     # Test files
├── 📄 requirements.txt           # Python dependencies
├── 📄 setup.py                   # Package setup
├── 📄 pyproject.toml            # Modern Python packaging
└── 📄 README.md                 # This file
```

## Analysis Reports

### What Rosetta Analyzes

- **File Statistics**: Total files scanned and translation instances found
- **Key Conflicts**: Same translation key with different values
- **Exact Redundancy**: Different keys with identical static text
- **Pattern Redundancy**: Different keys with same dynamic patterns
- **Scanning Errors**: Files that couldn't be processed

### Sample Output

```
===== Report =====
Total files scanned: 45
Total instances found: 127
Key conflicts (same key, different values): 2
Exact value redundancy (same static text): 5
Pattern redundancy (same dynamic pattern): 3
Errors: 0

-- Key Conflicts (same key, different values) --
'user.welcome': ['Welcome', 'Welcome!']

-- Exact Value Redundancy (different keys, same static text) --
'Loading...': ['app.loading', 'common.loading', 'ui.loading']
```

## Excel Output

When using `--excel`, Rosetta creates organized Excel files:

### File Organization
- **Default Output**: Files saved to `output/output-DD-MM-YYYY-HH-MM/` (automatically timestamped)
- **Separate files per prefix**: `auth_translations.xlsx`, `user_translations.xlsx`, etc.
- **Columns**: Key, EN (English), DK, SW, ES, PG
- **Smart grouping**: Related translations grouped by key prefix

### AI Translation
With `--translate` flag:
- Automatically fills target language columns
- Uses OpenAI GPT-3.5-turbo for high-quality translations
- Maintains placeholders like `{name}`, `{count}` unchanged
- Provides token usage statistics

## Configuration

### Environment Variables

```bash
# Required for AI translation
export OPENAI_API_KEY="your-openai-api-key-here"
```

**⚠️ Security Note:** Never commit your API keys to version control. Use environment variables or a `.env` file (which is in `.gitignore`).

### Custom Configuration

Edit `src/config/settings.py` to customize:

- **Target Languages**: Add/remove translation languages
- **File Extensions**: Change which file types to scan
- **OpenAI Settings**: Model, temperature, token limits
- **Translation Patterns**: Modify regex patterns

## Installation as Package

### Development Installation

```bash
pip install -e .
```

### Use as Installed Command

After installation:

```bash
rosetta /path/to/project --excel --translate
```

## Backward Compatibility

The original `rosetta.py` file still works but shows a deprecation warning:

```bash
# Still works but deprecated
python rosetta.py /path/to/project --excel
```

## Testing

Run tests (when available):

```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Tips & Best Practices

### Before Running
- Ensure your translation keys follow a consistent naming convention
- Use prefixes to organize translations (e.g., `auth.login`, `user.profile`)
- Test with a small folder first to understand the output

### Using AI Translation
- Review AI translations for context and accuracy
- Consider your target audience and cultural nuances
- Use the preview mode first to check translation keys

### Managing Large Projects
- Excel files are automatically organized in timestamped folders (output/output-DD-MM-YYYY-HH-MM)
- Use `--output-dir` to specify custom output directories
- Run analysis first without `--excel` to identify conflicts
- Fix conflicts before generating final Excel files

## Troubleshooting

### Common Issues

**OpenAI API Error**: Ensure your API key is valid and has sufficient credits.
```bash
export OPENAI_API_KEY="your-valid-api-key"
```

**File Permission Error**: Ensure you have read access to the target folder.

**Large Output**: Use `--extensions` to limit file types or scan smaller folders.

### Getting Help

- Check the console output for detailed error messages
- Use `--log` for verbose scanning information
- Review generated Excel files for data accuracy

## 🛠️ Development Setup

For contributors and developers:

```bash
# Quick setup with the automated script
./setup.sh

# Manual setup
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
```

**Security Notes:**
- Never commit API keys to version control
- The `.env` file is automatically ignored by git
- Use environment variables in production

---

