# Clipping Archive Scripts

This repository contains scripts to help organize your clippings into a structured archive system.

## Simplified 3-Step Organization Process

### Step 1: Generate Categorization Template

Run the `create_categorization_file.sh` script to generate a template listing all your clippings:

```bash
./create_categorization_file.sh
```

This creates a file named `categorize_all.txt` that lists all markdown files in your Clippings directory with placeholder categories.

### Step 2: Edit the Categorization File

Edit the `categorize_all.txt` file to assign appropriate categories to each file. The format is:

```
filename.md|primary_category/subcategory|secondary_category/subcategory
```

You can edit this file manually or get AI assistance (see prompt template below).

### Step 3: Run the Organization Script

Execute the `organize_files.py` script to move files based on your categorization:

```bash
python3 organize_files.py
```

This will:
1. Create necessary category directories
2. Move files to their primary categories
3. Create symbolic links for secondary categories (if specified)
4. Display a summary of processed files

The Python script includes several improvements:
- Robust handling of special characters and Unicode in filenames
- Fuzzy matching to handle slight filename variations
- Better error handling and reporting
- Support for both primary and secondary categories

## Available Categories

- **AI and Technology**
  - `AI-and-Technology/AI-Limitations`
  - `AI-and-Technology/Tech-Competition`
  - `AI-and-Technology/Privacy-Surveillance`
  - `AI-and-Technology/Open-Source-AI`

- **Media and Communication**
  - `Media-and-Communication/Media-Transformation`
  - `Media-and-Communication/Social-Platforms`
  - `Media-and-Communication/Communication-Frameworks`

- **Business and Finance**
  - `Business-and-Finance/Luxury-Markets`
  - `Business-and-Finance/Corporate-Ethics`
  - `Business-and-Finance/Marketing-Strategy`

- **Society and Human Understanding**
  - `Society-and-Human-Understanding/Dehumanization-Propaganda`
  - `Society-and-Human-Understanding/Impact-vs-Intent`
  - `Society-and-Human-Understanding/Religion-Narratives`

- **Personal Development**
  - `Personal-Development/Generalist-Resources`
  - `Personal-Development/Neurodiversity-Tools`

## AI Prompt for Categorization Assistance

If you need help categorizing your clippings, paste the following prompt along with your `categorize_all.txt` file to an AI assistant:

```
I need help categorizing these files for my personal archive system. 
Please assign appropriate categories to these clippings to the best of your ability.

Each line should follow this format:
filename.md|primary_category/subcategory|optional_secondary_category/subcategory

The primary categories and subcategories should be selected from:

AI-and-Technology/AI-Limitations
AI-and-Technology/Tech-Competition
AI-and-Technology/Privacy-Surveillance
AI-and-Technology/Open-Source-AI
Media-and-Communication/Media-Transformation
Media-and-Communication/Social-Platforms
Media-and-Communication/Communication-Frameworks
Business-and-Finance/Luxury-Markets
Business-and-Finance/Corporate-Ethics
Business-and-Finance/Marketing-Strategy
Society-and-Human-Understanding/Dehumanization-Propaganda
Society-and-Human-Understanding/Impact-vs-Intent
Society-and-Human-Understanding/Religion-Narratives
Personal-Development/Generalist-Resources
Personal-Development/Neurodiversity-Tools

Please review each filename and categorize based on what you think would be most appropriate.
If a file belongs in multiple categories, use the secondary category field.
Leave files marked as CATEGORY if you're unsure about their categorization.
```

## Example Categorization

Here's an example of how entries in your categorization file should look:

```
# AI Technology examples
'You Can't Lick a Badger Twice' Google Failures Highlight a Fundamental AI Flaw.md|AI-and-Technology/AI-Limitations|
AI Can Fix Social Media's Original Sin.md|AI-and-Technology/Tech-Competition|Media-and-Communication/Social-Platforms

# Media examples
Meta's Monopoly Made It a Fair-Weather Friend.md|Media-and-Communication/Social-Platforms|Business-and-Finance/Corporate-Ethics
YouTube turns 20 and is on track to be the biggest media company by revenue.md|Media-and-Communication/Media-Transformation|

# Files to skip for now
some-reference-file.md|CATEGORY|
```

## Adding New Categories

If you need to add new categories to the archive system:

1. Create the new directory structure in the `Archives` folder
2. Update the category list in `create_categorization_file.sh`
3. Create a README.md file in the new category explaining its purpose

## Troubleshooting

If you encounter any issues with file organization:

1. **File Not Found**: The script uses fuzzy matching to handle special characters and slight variations in filenames. If a file is still not found, check that:
   - The file exists in the Clippings directory
   - The filename in categorize_all.txt matches the actual file (ignoring special characters)
   - The file hasn't already been moved to the Archives directory

2. **Permission Errors**: Make sure you have write permissions for both the Clippings and Archives directories

3. **Symbolic Link Issues**: On Windows, you may need to run the script with administrator privileges to create symbolic links
