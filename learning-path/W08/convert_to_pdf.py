#!/usr/bin/env python3
"""
Convert Markdown report to PDF with proper formatting, images, and links.
"""

import os
import re
from pathlib import Path
from markdown import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def process_markdown_to_html(md_file_path):
    """Convert Markdown to HTML with proper image paths and styling."""
    
    # Read the markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Get the directory of the markdown file for resolving relative paths
    md_dir = Path(md_file_path).parent
    
    # Fix image paths - ensure they're relative to the markdown file location
    def fix_image_path(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        # If it's already a relative path, make it absolute relative to md_dir
        if not img_path.startswith('http'):
            full_path = md_dir / img_path
            if full_path.exists():
                # Use absolute file path for weasyprint
                return f'![{alt_text}]({full_path.absolute()})'
            else:
                print(f"Warning: Image not found: {full_path}")
        return match.group(0)
    
    # Fix image references in markdown (corrected regex groups)
    md_content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', fix_image_path, md_content)
    
    # Convert HTML div page breaks to markdown-compatible format
    # This will be handled after HTML conversion
    md_content = md_content.replace('<div style="page-break-before: always;"></div>', 
                                   '\n\n<div class="page-break"></div>\n\n')
    
    # Convert markdown to HTML
    html_content = markdown(md_content, extensions=[
        'extra',  # For tables, fenced code blocks, etc.
        'codehilite',  # For syntax highlighting
        'tables',  # For better table support
        'nl2br',  # Convert newlines to <br>
    ])
    
    # Post-process HTML to fix image paths
    def fix_html_image_path(match):
        img_tag = match.group(0)
        src = match.group(1)
        # Convert relative paths to absolute file paths
        if src and not src.startswith('http') and not src.startswith('file://'):
            # Handle both relative and absolute paths
            if os.path.isabs(src):
                img_path = Path(src)
            else:
                img_path = md_dir / src
            if img_path.exists():
                # Use absolute path (weasyprint handles this better)
                new_src = str(img_path.absolute())
                print(f"  ✓ Found image: {img_path.name}")
                return img_tag.replace(f'src="{src}"', f'src="{new_src}"')
            else:
                print(f"  ✗ Image not found: {img_path}")
        return img_tag
    
    # Fix image src attributes in HTML
    print("Processing images...")
    html_content = re.sub(r'<img[^>]+src="([^"]+)"[^>]*>', fix_html_image_path, html_content)
    
    # Create full HTML document with CSS
    css_style = """
    <style>
        @page {
            size: A4;
            margin: 2cm;
            @top-center {
                content: "W8 L1 Group Task Report";
                font-size: 9pt;
                color: #666;
            }
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
            }
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
        }
        
        h1 {
            font-size: 24pt;
            color: #1a1a1a;
            margin-top: 30pt;
            margin-bottom: 15pt;
            page-break-after: avoid;
            border-bottom: 2px solid #1a1a1a;
            padding-bottom: 10pt;
        }
        
        h2 {
            font-size: 18pt;
            color: #2a2a2a;
            margin-top: 25pt;
            margin-bottom: 12pt;
            page-break-after: avoid;
        }
        
        h3 {
            font-size: 14pt;
            color: #3a3a3a;
            margin-top: 20pt;
            margin-bottom: 10pt;
            page-break-after: avoid;
        }
        
        h4 {
            font-size: 12pt;
            color: #4a4a4a;
            margin-top: 15pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
        }
        
        p {
            margin-bottom: 10pt;
            text-align: justify;
        }
        
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 15pt auto;
            page-break-inside: avoid;
            page-break-after: avoid;
        }
        
        /* Keep images with their captions */
        img + em, img + p, img + i {
            page-break-before: avoid;
            text-align: center;
            font-style: italic;
            font-size: 9pt;
            color: #666;
            margin-top: 5pt;
            margin-bottom: 15pt;
            display: block;
        }
        
        /* Ensure images don't get cut at page boundaries */
        img {
            page-break-before: auto;
            page-break-after: auto;
            page-break-inside: avoid;
        }
        
        /* Keep image and caption together */
        p:has(img), div:has(img) {
            page-break-inside: avoid;
        }
        
        /* Page breaks */
        .page-break {
            page-break-before: always;
        }
        
        /* Keep sections together when possible */
        h2, h3 {
            page-break-after: avoid;
        }
        
        /* Don't break code blocks */
        pre {
            page-break-inside: avoid;
            background-color: #f5f5f5;
            padding: 10pt;
            border-radius: 4pt;
            overflow-x: auto;
            font-size: 9pt;
        }
        
        code {
            background-color: #f5f5f5;
            padding: 2pt 4pt;
            border-radius: 3pt;
            font-size: 10pt;
        }
        
        /* Table styling */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15pt 0;
            page-break-inside: avoid;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8pt;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        /* Links */
        a {
            color: #0066cc;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        /* Lists */
        ul, ol {
            margin-bottom: 10pt;
            padding-left: 25pt;
        }
        
        li {
            margin-bottom: 5pt;
        }
        
        /* Blockquotes */
        blockquote {
            border-left: 4px solid #ddd;
            padding-left: 15pt;
            margin: 15pt 0;
            color: #666;
            font-style: italic;
        }
        
        /* Horizontal rules */
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 20pt 0;
        }
        
        /* Keep example sections together */
        .example-section {
            page-break-inside: avoid;
        }
        
        /* Ensure figures don't break across pages */
        figure {
            page-break-inside: avoid;
            margin: 15pt 0;
        }
    </style>
    """
    
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>W8 L1 Group Task Report</title>
    {css_style}
</head>
<body>
    {html_content}
</body>
</html>"""
    
    return full_html

def convert_to_pdf(md_file_path, output_pdf_path):
    """Convert Markdown file to PDF."""
    
    print(f"Converting {md_file_path} to PDF...")
    
    # Get the directory of the markdown file for base URL
    md_dir = Path(md_file_path).parent
    
    # Convert markdown to HTML
    html_content = process_markdown_to_html(md_file_path)
    
    # Convert HTML to PDF
    print("Generating PDF...")
    # Use the markdown file directory as base_url for resolving relative image paths
    base_url = f"file://{md_dir.absolute()}/"
    
    HTML(string=html_content, base_url=base_url).write_pdf(
        output_pdf_path,
        stylesheets=[],
    )
    
    print(f"✅ PDF created successfully: {output_pdf_path}")

if __name__ == "__main__":
    # Get the directory of this script
    script_dir = Path(__file__).parent
    md_file = script_dir / "W8_L1_Report.md"
    pdf_file = script_dir / "W8_L1_Report.pdf"
    
    if not md_file.exists():
        print(f"Error: {md_file} not found!")
        exit(1)
    
    convert_to_pdf(md_file, pdf_file)
    print(f"\n✅ Conversion complete! PDF saved to: {pdf_file}")
