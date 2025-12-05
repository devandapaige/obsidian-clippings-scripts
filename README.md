# Archives

This folder contains my **initial thoughts and intuition** captured after reading or watching longer-form content, organized by category.

## Purpose

Instead of saving full articles or complete transcripts, I capture:
- My immediate reactions and insights
- Key takeaways that resonate with me
- Questions that arise
- Connections to other ideas
- Personal reflections on the content

This approach helps me:
- Focus on what actually matters to me
- Build a knowledge base of my own thinking
- Avoid information overload
- Create a more personal and useful archive

## Organization

Content is organized into the following categories:

### AI-and-Technology
- **AI-Limitations**: Articles about AI constraints, failures, or limitations
- **Tech-Competition**: Industry competition, market dynamics, tech company strategies
- **Privacy-Surveillance**: Privacy concerns, surveillance, data collection
- **Open-Source-AI**: Open source AI projects, community initiatives

### Media-and-Communication
- **Media-Transformation**: How media is changing, new formats, industry shifts
- **Social-Platforms**: Social media platforms, their impact, changes
- **Communication-Frameworks**: Communication theory, frameworks, best practices

### Business-and-Finance
- **Luxury-Markets**: Luxury goods, high-end markets, premium brands
- **Corporate-Ethics**: Corporate responsibility, ethical business practices
- **Marketing-Strategy**: Marketing approaches, branding, customer engagement

### Society-and-Human-Understanding
- **Dehumanization-Propaganda**: Dehumanizing narratives, propaganda, harmful messaging
- **Impact-vs-Intent**: Understanding impact regardless of intent, accountability
- **Religion-Narratives**: Religious themes, spiritual narratives, belief systems

### Personal-Development
- **Generalist-Resources**: General productivity, career advice, life skills
- **Neurodiversity-Tools**: Resources for neurodivergent individuals, masking, ADHD, autism

## Workflow

1. **Capture**: When I read or watch something that sparks thoughts, I create a note in the `Clippings` folder
2. **Reflect**: I write down my initial thoughts, intuitions, and reactions
3. **Categorize**: I assign the appropriate category using the categorization file
4. **Organize**: The `organize_files.py` script moves the file to the correct Archive subdirectory
5. **Index**: The script automatically adds your insights to `INSIGHTS.md` for easy reference

## Insights Index

The `INSIGHTS.md` file in this directory is automatically maintained and contains a chronological index of all your insights. Each entry includes:
- **Title**: The title of the content (extracted from frontmatter)
- **Date**: The date you captured the insight (from `created` or `published` field)
- **Your thoughts**: Your full personal reflections and insights
- **File location**: Clickable path to the original file for easy access

This creates a single searchable document of all your insights that you can reference when creating content. The index is automatically updated whenever you organize clippings—no manual work required.

### Quarterly Archiving

You can rename and archive this file quarterly (e.g., `INSIGHTS-2025-Q4.md`) and start fresh. The script will automatically create a new `INSIGHTS.md` for the next quarter.

## File Format

Each file includes:
- **Frontmatter**: Title, source URL, author, publication date, description, tags
- **Content**: My personal thoughts, reactions, and insights (not the full article)

Example:
```markdown
---
title: "Article Title"
source: "https://example.com/article"
author: "[[Author Name]]"
published: 2025-12-05
created: 2025-12-05
description: "Brief description"
tags:
  - "clippings"
---

My initial thoughts and reactions go here...
```

## Scripts

- **`create_categorization_file.sh`**: Generates a template file (`categorize_all.txt`) listing all clippings for categorization
- **`organize_files.py`**: 
  - Moves categorized files from Clippings to the appropriate Archive subdirectory
  - Automatically extracts and indexes insights to `INSIGHTS.md`
  - Includes duplicate prevention
  - Verifies file integrity before removing originals

### Usage

```bash
# Step 1: Generate categorization template
bash create_categorization_file.sh

# Step 2: Edit categorize_all.txt to add categories
# Format: filename|primary_category|secondary_category

# Step 3: Organize files (moves files and updates insights index)
python3 organize_files.py categorize_all.txt
```

