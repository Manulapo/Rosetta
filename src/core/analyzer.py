"""Translation analysis functionality for detecting conflicts and redundancy."""

import re
from typing import List, Tuple, Dict, Set
from collections import defaultdict


def normalize_dynamic_value(value: str) -> str:
    """
    Normalize values with variables like 'Battery level: {value}%' 
    to a pattern for comparison purposes.
    
    Args:
        value: Original translation value
        
    Returns:
        Normalized value with variables replaced by {VAR}
    """
    # Replace variable placeholders with a generic marker
    normalized = re.sub(r'\{[^}]+\}', '{VAR}', value)
    return normalized


def analyze_translations(all_translations: List[Tuple[str, str]]) -> Dict:
    """
    Analyze translations for conflicts and redundancy.
    
    Args:
        all_translations: List of (key, value) translation pairs
        
    Returns:
        Dictionary containing analysis results:
        - conflicts: Same key with different values
        - exact_redundancy: Different keys with same static text
        - pattern_redundancy: Different keys with same dynamic pattern
    """
    # Group by key to find same key with different values (conflicts)
    key_to_values = defaultdict(set)
    for k, v in all_translations:
        key_to_values[k].add(v)
    conflicts = {k: vals for k, vals in key_to_values.items() if len(vals) > 1}
    
    # Group by normalized value to find different keys with same value pattern (redundancy)
    # This treats 'Hello {name}' and 'Hello {user}' as the same pattern
    normalized_value_to_keys = defaultdict(set)
    original_value_to_keys = defaultdict(set)
    
    for k, v in all_translations:
        normalized_v = normalize_dynamic_value(v)
        normalized_value_to_keys[normalized_v].add(k)
        original_value_to_keys[v].add(k)
    
    # Find redundancy in normalized patterns (dynamic values)
    pattern_redundancy = {v: keys for v, keys in normalized_value_to_keys.items() if len(keys) > 1}
    
    # Find exact value redundancy (static values)
    exact_redundancy = {v: keys for v, keys in original_value_to_keys.items() if len(keys) > 1}
    
    return {
        'conflicts': conflicts,
        'exact_redundancy': exact_redundancy,
        'pattern_redundancy': pattern_redundancy
    }


def group_translations_by_prefix(all_translations: List[Tuple[str, str]]) -> Dict[str, Dict[str, str]]:
    """
    Group translations by prefix (first part before the dot).
    
    Args:
        all_translations: List of (key, value) translation pairs
        
    Returns:
        Dictionary mapping prefix to dictionary of unique key-value pairs
    """
    prefix_groups = defaultdict(dict)
    
    for key, value in all_translations:
        # Get prefix (everything before the first dot)
        prefix = key.split('.')[0] if '.' in key else key
        
        # Store unique key-value pairs for this prefix
        if key not in prefix_groups[prefix]:
            prefix_groups[prefix][key] = value
    
    return prefix_groups


def print_preview(all_translations: List[Tuple[str, str]]) -> None:
    """
    Print all dictionary entries grouped by prefix (first part before dot).
    
    Args:
        all_translations: List of (key, value) translation pairs
    """
    prefix_groups = group_translations_by_prefix(all_translations)
    
    print("\n===== PREVIEW: All Translation Dictionaries =====")
    print(f"Total unique translations found: {sum(len(translations) for translations in prefix_groups.values())}")
    print(f"Number of prefix groups: {len(prefix_groups)}")
    
    # Sort prefixes alphabetically for consistent output
    for prefix in sorted(prefix_groups.keys()):
        translations = prefix_groups[prefix]
        print(f"\n--- {prefix.upper()} ({len(translations)} translations) ---")
        
        # Sort keys alphabetically within each prefix group
        for key in sorted(translations.keys()):
            value = translations[key]
            print(f"'{key}': '{value}'")
    
    print(f"\n===== END PREVIEW =====")


def generate_report(
    all_translations: List[Tuple[str, str]], 
    file_counts: Dict[str, int], 
    errors: List[str],
    preview_mode: bool = False
) -> Dict:
    """
    Generate a comprehensive analysis report.
    
    Args:
        all_translations: List of (key, value) translation pairs
        file_counts: Dictionary mapping file paths to translation counts
        errors: List of error messages
        preview_mode: Whether to show preview instead of report
        
    Returns:
        Dictionary containing report data
    """
    total_instances = len(all_translations)
    
    # If preview mode is enabled, show grouped translations and exit
    if preview_mode:
        print_preview(all_translations)
        return {}
    
    analysis = analyze_translations(all_translations)
    conflicts = analysis['conflicts']
    exact_redundancy = analysis['exact_redundancy']
    pattern_redundancy = analysis['pattern_redundancy']

    print("\n===== Report =====")
    print(f"Total files scanned: {len(file_counts)}")
    print(f"Total instances found: {total_instances}")
    print(f"Key conflicts (same key, different values): {len(conflicts)}")
    print(f"Exact value redundancy (same static text): {len(exact_redundancy)}")
    print(f"Pattern redundancy (same dynamic pattern): {len(pattern_redundancy)}")
    print(f"Errors: {len(errors)}")

    if conflicts:
        print("\n-- Key Conflicts (same key, different values) --")
        for k, vals in conflicts.items():
            print(f"'{k}': {list(vals)}")

    if exact_redundancy:
        print("\n-- Exact Value Redundancy (different keys, same static text) --")
        for v, keys in exact_redundancy.items():
            print(f"'{v}': {list(keys)}")
    
    if pattern_redundancy:
        print("\n-- Pattern Redundancy (different keys, same dynamic pattern) --")
        for pattern, keys in pattern_redundancy.items():
            if pattern not in exact_redundancy:  # Don't show if already shown in exact redundancy
                # Find original values for this pattern
                original_values = [v for k, v in all_translations if k in keys and normalize_dynamic_value(v) == pattern]
                print(f"Pattern '{pattern}':")
                print(f"  Keys: {list(keys)}")
                print(f"  Original values: {list(set(original_values))}")

    if errors:
        print("\n-- Errors --")
        for err in errors:
            print(err)
    
    return {
        'total_instances': total_instances,
        'total_files': len(file_counts),
        'conflicts': conflicts,
        'exact_redundancy': exact_redundancy,
        'pattern_redundancy': pattern_redundancy,
        'errors': errors
    }