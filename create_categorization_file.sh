#!/bin/bash

# Creates a template file listing all clippings for you to categorize

OUTPUT_FILE="categorize_all.txt"

echo "# Format: filename|primary_category|secondary_category" > $OUTPUT_FILE
echo "# Primary categories should be one of:" >> $OUTPUT_FILE
echo "# AI-and-Technology/AI-Limitations" >> $OUTPUT_FILE
echo "# AI-and-Technology/Tech-Competition" >> $OUTPUT_FILE 
echo "# AI-and-Technology/Privacy-Surveillance" >> $OUTPUT_FILE
echo "# AI-and-Technology/Open-Source-AI" >> $OUTPUT_FILE
echo "# Media-and-Communication/Media-Transformation" >> $OUTPUT_FILE
echo "# Media-and-Communication/Social-Platforms" >> $OUTPUT_FILE
echo "# Media-and-Communication/Communication-Frameworks" >> $OUTPUT_FILE
echo "# Business-and-Finance/Luxury-Markets" >> $OUTPUT_FILE
echo "# Business-and-Finance/Corporate-Ethics" >> $OUTPUT_FILE
echo "# Business-and-Finance/Marketing-Strategy" >> $OUTPUT_FILE
echo "# Society-and-Human-Understanding/Dehumanization-Propaganda" >> $OUTPUT_FILE
echo "# Society-and-Human-Understanding/Impact-vs-Intent" >> $OUTPUT_FILE
echo "# Society-and-Human-Understanding/Religion-Narratives" >> $OUTPUT_FILE
echo "# Personal-Development/Generalist-Resources" >> $OUTPUT_FILE
echo "# Personal-Development/Neurodiversity-Tools" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# Get all markdown files in the Clippings directory
find Clippings -name "*.md" -type f | sort | while read -r file; do
    filename=$(basename "$file")
    echo "$filename|CATEGORY|" >> $OUTPUT_FILE
done

echo "Created $OUTPUT_FILE with all clippings."
echo "Now edit this file to add categories, then run the organize_all.sh script." 