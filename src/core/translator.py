"""OpenAI translation functionality."""

import time
from typing import Dict, List, Tuple, Optional
from openai import OpenAI

from ..config import (
    OPENAI_API_KEY,
    LANGUAGE_CODES,
    DEFAULT_TARGET_LANGUAGES,
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
    OPENAI_MAX_TOKENS,
    TRANSLATIONS_PER_BATCH,
    DELAY_BETWEEN_BATCHES,
)


# Initialize OpenAI client with the API key (if available)
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def check_openai_api_key() -> Tuple[bool, str]:
    """
    Check if OpenAI API key is available and valid.
    
    Returns:
        Tuple of (is_valid, status_message)
    """
    if not OPENAI_API_KEY:
        return False, "❌ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
    
    if OPENAI_API_KEY == "your-api-key-here":
        return False, "⚠️  Please replace 'your-api-key-here' with your actual OpenAI API key in the script"
    
    try:
        # Test the API key by making a simple request
        client.models.list()
        return True, "✅ OpenAI API key is valid and ready"
    except Exception as e:
        return False, f"❌ OpenAI API key error: {e}"


def translate_with_openai(
    text: str, 
    target_language: str, 
    context: str = "property management application"
) -> Tuple[str, Optional[object]]:
    """
    Translate text to target language using OpenAI GPT.
    
    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'DK', 'SW')
        context: Context for better translation
        
    Returns:
        Tuple of (translated_text, token_usage)
    """
    target_lang_name = LANGUAGE_CODES.get(target_language, target_language)
    
    prompt = f"""You are a professional translator for software user interfaces.

Task:
Translate the following English text into {target_lang_name}. 
Context: {context}.

CRITICAL RULES:
- NEVER translate anything inside curly brackets {{}}. Keep ALL curly bracket placeholders EXACTLY as they are.
- Examples: {{name}}, {{count}}, {{username}}, {{value}} must remain unchanged.
- Only translate the text outside the curly brackets.

Guidelines:
- Match the tone of modern app UI: clear, concise, and natural.
- Prefer common, widely used terms in {target_lang_name} instead of literal translations.
- If the input is a single word, output a single word.
- Output ONLY the translation text. No quotes, no extra words.

English: {text}"""

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional translator specializing in software UI translations."},
                {"role": "user", "content": prompt}
            ],
            temperature=OPENAI_TEMPERATURE,
            max_tokens=OPENAI_MAX_TOKENS
        )
        
        translation = response.choices[0].message.content.strip()
        
        # Clean up the response to get just the translation
        if translation.startswith('"') and translation.endswith('"'):
            translation = translation[1:-1]
        
        # Get token usage from response
        token_usage = response.usage
        
        return translation, token_usage
        
    except Exception as e:
        return f"Translation error: {e}", None


def translate_batch_with_openai(
    translations_dict: Dict[str, str], 
    target_languages: List[str] = None
) -> List[Dict[str, str]]:
    """
    Translate all English texts to target languages using OpenAI.
    
    Args:
        translations_dict: Dictionary mapping keys to English text
        target_languages: List of target language codes
        
    Returns:
        List of dictionaries containing translations for each language
    """
    if target_languages is None:
        target_languages = DEFAULT_TARGET_LANGUAGES.copy()
        
    translated_data = []
    total_translations = len(translations_dict)
    
    # Token usage tracking
    total_tokens = 0
    total_prompt_tokens = 0
    total_completion_tokens = 0
    
    print(f"\n🌐 Starting OpenAI translation of {total_translations} texts to {len(target_languages)} languages...")
    print("⏳ This may take a few minutes...")
    
    for i, (key, english_text) in enumerate(translations_dict.items(), 1):
        print(f"📝 Translating {i}/{total_translations}: '{key[:50]}{'...' if len(key) > 50 else ''}'")
        
        row_data = {
            'key': key,
            'en': english_text
        }
        
        # Translate to each target language
        for lang in target_languages:
            print(f"  → {lang}...", end=' ')
            translation, token_usage = translate_with_openai(english_text, lang)
            
            # Track token usage if available
            if token_usage:
                total_tokens += token_usage.total_tokens
                total_prompt_tokens += token_usage.prompt_tokens
                total_completion_tokens += token_usage.completion_tokens
            
            row_data[lang] = translation
            print("✓")
        
        translated_data.append(row_data)
        
        # Small delay to avoid rate limiting
        if i % TRANSLATIONS_PER_BATCH == 0:
            print(f"  ⏸️  (Completed {i}/{total_translations} translations)")
            time.sleep(DELAY_BETWEEN_BATCHES)
    
    print(f"\n✅ OpenAI translation complete! Processed {total_translations} texts")
    print(f"\n📊 Token usage summary:")
    print(f"  • Total tokens used: {total_tokens:,}")
    print(f"  • Prompt tokens: {total_prompt_tokens:,}")
    print(f"  • Completion tokens: {total_completion_tokens:,}")
    if total_translations > 0 and len(target_languages) > 0:
        avg_tokens = total_tokens // (total_translations * len(target_languages))
        print(f"  • Average tokens per translation: {avg_tokens}")
    
    return translated_data