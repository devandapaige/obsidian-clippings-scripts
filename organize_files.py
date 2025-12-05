#!/usr/bin/env python3
"""
Organize clippings (initial thoughts/intuitions) from Clippings folder into Archives.

These files contain personal reflections captured after reading/watching longer-form content,
not full articles. They are organized by category into the Archives folder structure.
"""
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

def extract_insights_from_file(filepath: str) -> Tuple[str, str, Optional[str]]:
    """
    Extract title, user's thoughts, and date from a clipping file.
    Returns (title, thoughts, date) tuple.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title and date from frontmatter
        title = None
        date = None
        if content.startswith('---'):
            # Find the end of frontmatter
            end_idx = content.find('---', 3)
            if end_idx != -1:
                frontmatter = content[3:end_idx]
                # Look for title and date fields
                for line in frontmatter.split('\n'):
                    if line.startswith('title:'):
                        title = line.split('title:', 1)[1].strip().strip('"').strip("'")
                    elif line.startswith('created:'):
                        date = line.split('created:', 1)[1].strip()
                    elif line.startswith('published:') and not date:
                        # Use published date if created date not available
                        date = line.split('published:', 1)[1].strip()
        
        # Extract thoughts (content after frontmatter)
        thoughts = ""
        if content.startswith('---'):
            end_idx = content.find('---', 3)
            if end_idx != -1:
                thoughts = content[end_idx + 3:].strip()
        else:
            thoughts = content.strip()
        
        # If no title found, use filename without extension
        if not title:
            title = os.path.splitext(os.path.basename(filepath))[0]
        
        return title, thoughts, date
    except Exception as e:
        # Fallback to filename if extraction fails
        title = os.path.splitext(os.path.basename(filepath))[0]
        return title, "", None

def append_to_insights_index(title: str, thoughts: str, file_path: str, date: Optional[str] = None):
    """Append an entry to the insights index file, avoiding duplicates."""
    insights_file = os.path.join('Archives', 'INSIGHTS.md')
    
    # Check if entry already exists
    entry_exists = False
    if os.path.exists(insights_file):
        with open(insights_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check if this title already exists
            if f"## {title}\n" in content:
                entry_exists = True
    
    # Skip if entry already exists
    if entry_exists:
        return
    
    # Create file with header if it doesn't exist
    if not os.path.exists(insights_file):
        with open(insights_file, 'w', encoding='utf-8') as f:
            f.write("# Archives Insights Index\n\n")
            f.write("This file contains a chronological index of all your insights and thoughts from consumed content.\n\n")
            f.write("---\n\n")
    
    # Format date if available
    date_str = ""
    if date:
        date_str = f"**Date:** {date}\n\n"
    
    # Append new entry
    with open(insights_file, 'a', encoding='utf-8') as f:
        f.write(f"## {title}\n\n")
        if date_str:
            f.write(date_str)
        if thoughts:
            # Show full thoughts (these are your personal insights, so keep them complete)
            f.write(f"{thoughts}\n\n")
        f.write(f"📍 `Archives/{file_path}`\n\n")
        f.write("---\n\n")

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
    """
    Main function to organize clippings (initial thoughts/intuitions) into Archives.
    
    Moves files from Clippings directory to appropriate Archive subdirectories
    based on the categorization file. Files contain personal reflections, not full articles.
    """
    if not os.path.exists('Clippings'):
        print("Error: Clippings directory not found!")
        return
    
    # Check if Clippings directory is empty
    clippings_files = [f for f in os.listdir('Clippings') if not f.startswith('.') and f.endswith('.md')]
    if not clippings_files:
        print("Warning: Clippings directory appears to be empty!")
        print("This might mean files were already moved. Checking Archives...")
        # Count files in Archives that match our categorization
        entries = parse_categorization_file(categorization_file)
        found_count = 0
        for filename, primary, _ in entries:
            archive_path = os.path.join('Archives', primary, filename)
            if os.path.exists(archive_path):
                found_count += 1
        if found_count > 0:
            print(f"Found {found_count}/{len(entries)} files already in Archives.")
            print("Files may have already been organized. Exiting to prevent duplicate processing.")
            return
        else:
            print("No matching files found in Archives. Proceeding anyway...")

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
            
            # Verify copy succeeded before removing original
            if not os.path.exists(primary_path):
                raise Exception(f"Copy verification failed: {primary_path} does not exist")
            
            # Verify file sizes match (basic integrity check)
            source_size = os.path.getsize(source_path)
            dest_size = os.path.getsize(primary_path)
            if source_size != dest_size:
                raise Exception(f"Copy verification failed: size mismatch (source: {source_size}, dest: {dest_size})")
            
            # Only remove original after successful copy and verification
            os.remove(source_path)
            print(f"  → Copied to Archives/{primary}/")
            stats['moved'] += 1
            
            # Extract insights and append to insights index
            title, thoughts, date = extract_insights_from_file(primary_path)
            archive_path = f"{primary}/{actual_filename}"
            append_to_insights_index(title, thoughts, archive_path, date)
            print(f"  → Added to insights index")
            
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