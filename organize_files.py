#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def parse_categorization_file(filepath: str) -> List[Tuple[str, str, Optional[str]]]:
    """Parse the categorization file and return list of (filename, primary, secondary) tuples."""
    entries = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('|')
            if len(parts) >= 2:
                filename = parts[0].strip()
                primary = parts[1].strip()
                secondary = parts[2].strip() if len(parts) > 2 else None
                if primary and primary != 'CATEGORY':
                    entries.append((filename, primary, secondary))
    return entries

def normalize_filename(filename: str) -> str:
    """Normalize filename for comparison."""
    # Remove common punctuation and whitespace
    normalized = filename.lower()
    normalized = ''.join(c for c in normalized if c.isalnum() or c in [' ', '-'])
    normalized = ' '.join(normalized.split())
    return normalized

def find_matching_file(filename: str, directory: str) -> Optional[str]:
    """Find a matching file in directory using fuzzy matching."""
    normalized_target = normalize_filename(filename)
    best_match = None
    best_ratio = 0
    
    for actual_file in os.listdir(directory):
        if actual_file.startswith('.'):  # Skip hidden files
            continue
            
        normalized_actual = normalize_filename(actual_file)
        
        # Check if the normalized versions match at the start
        if normalized_actual.startswith(normalized_target[:50]) or normalized_target.startswith(normalized_actual[:50]):
            # Use the longer match ratio as the best match
            ratio = len(os.path.commonprefix([normalized_target, normalized_actual])) / max(len(normalized_target), len(normalized_actual))
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = actual_file
    
    # Only return a match if it's a good match (more than 80% similar)
    return best_match if best_ratio > 0.8 else None

def create_directory_structure():
    """Create the necessary directory structure."""
    base = Path('Archives')
    categories = {
        'AI-and-Technology': ['AI-Limitations', 'Tech-Competition', 'Privacy-Surveillance', 'Open-Source-AI'],
        'Media-and-Communication': ['Media-Transformation', 'Social-Platforms', 'Communication-Frameworks'],
        'Business-and-Finance': ['Luxury-Markets', 'Corporate-Ethics', 'Marketing-Strategy'],
        'Society-and-Human-Understanding': ['Dehumanization-Propaganda', 'Impact-vs-Intent', 'Religion-Narratives'],
        'Personal-Development': ['Generalist-Resources', 'Neurodiversity-Tools']
    }
    
    for category, subcategories in categories.items():
        for subcategory in subcategories:
            (base / category / subcategory).mkdir(parents=True, exist_ok=True)

def organize_files(categorization_file: str):
    """Main function to organize files."""
    if not os.path.exists('Clippings'):
        print("Error: Clippings directory not found!")
        return

    create_directory_structure()
    entries = parse_categorization_file(categorization_file)
    
    stats = {'moved': 0, 'linked': 0, 'skipped': 0}
    total = len(entries)
    
    for idx, (filename, primary, secondary) in enumerate(entries, 1):
        print(f"[{idx}/{total}] Processing: {filename}")
        
        # Find matching file in Clippings directory
        actual_filename = find_matching_file(filename, 'Clippings')
        if not actual_filename:
            print(f"  ✕ File not found in Clippings directory")
            stats['skipped'] += 1
            continue
            
        source_path = os.path.join('Clippings', actual_filename)
        primary_path = os.path.join('Archives', primary, actual_filename)
        
        # Create primary category directory if it doesn't exist
        os.makedirs(os.path.dirname(primary_path), exist_ok=True)
        
        try:
            # Copy file to primary category
            shutil.copy2(source_path, primary_path)
            os.remove(source_path)  # Remove original after successful copy
            print(f"  → Copied to Archives/{primary}/")
            stats['moved'] += 1
            
            # Handle secondary category if specified
            if secondary and secondary != 'CATEGORY':
                secondary_path = os.path.join('Archives', secondary)
                os.makedirs(secondary_path, exist_ok=True)
                
                # Calculate relative path for symlink
                rel_path = os.path.relpath(primary_path, secondary_path)
                link_path = os.path.join(secondary_path, actual_filename)
                
                # Create symlink
                if os.path.exists(link_path):
                    os.remove(link_path)
                os.symlink(rel_path, link_path)
                print(f"  → Linked to Archives/{secondary}/")
                stats['linked'] += 1
                
        except Exception as e:
            print(f"  ✕ Error processing file: {str(e)}")
            stats['skipped'] += 1
    
    print("\nOrganization complete!")
    print(f"  • Files moved: {stats['moved']}")
    print(f"  • Secondary links created: {stats['linked']}")
    print(f"  • Files skipped: {stats['skipped']}")

if __name__ == '__main__':
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'categorize_all.txt'
    organize_files(input_file) 