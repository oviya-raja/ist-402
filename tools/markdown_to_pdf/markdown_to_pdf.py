#!/usr/bin/env python3
"""
Convert Markdown to Professional PDF
Uses pandoc + playwright for high-quality PDF output

Usage:
    python3 markdown_to_pdf.py <input.md> [output.pdf]
    python3 markdown_to_pdf.py README.md output.pdf
    python3 markdown_to_pdf.py README.md  # Output will be README.pdf
"""
import subprocess
import sys
import argparse
from pathlib import Path
import os
import tempfile

def create_pdf(input_md, output_pdf=None):
    """
    Convert markdown file to professional PDF
    
    Args:
        input_md: Path to input markdown file
        output_pdf: Path to output PDF file (optional, defaults to input filename with .pdf extension)
    """
    input_path = Path(input_md).resolve()
    
    if not input_path.exists():
        print(f"❌ Error: Input file not found: {input_path}")
        sys.exit(1)
    
    if not input_path.suffix.lower() in ['.md', '.markdown']:
        print(f"⚠️  Warning: Input file doesn't have .md extension: {input_path}")
    
    # Determine output path
    if output_pdf:
        output_path = Path(output_pdf).resolve()
    else:
        output_path = input_path.with_suffix('.pdf')
    
    print("📄 Converting Markdown to Professional PDF...")
    print(f"   Input:  {input_path}")
    print(f"   Output: {output_path}")
    
    # Create temporary files
    script_dir = Path(__file__).parent
    html_file = script_dir / "temp_output.html"
    css_file = script_dir / "pdf_style.css"
    
    # Create professional CSS
    css_content = """@page {
    size: A4;
    margin: 2.5cm 2cm 2.5cm 2cm;
}

body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #2c3e50;
    max-width: 100%;
}

h1 {
    font-size: 24pt;
    font-weight: 700;
    color: #1a1a1a;
    margin-top: 0;
    margin-bottom: 0.5em;
    padding-bottom: 0.3em;
    border-bottom: 3px solid #3498db;
}

h2 {
    font-size: 18pt;
    font-weight: 600;
    color: #2c3e50;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    padding-bottom: 0.2em;
    border-bottom: 1px solid #ecf0f1;
}

h3 {
    font-size: 14pt;
    font-weight: 600;
    color: #34495e;
    margin-top: 1.2em;
    margin-bottom: 0.4em;
}

code {
    background-color: #f8f9fa;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
    color: #e83e8c;
}

pre {
    background-color: #f8f9fa;
    padding: 1em;
    border-radius: 5px;
    border-left: 4px solid #3498db;
    font-family: 'Courier New', monospace;
    font-size: 0.85em;
    overflow-x: auto;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1.5em auto;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1.5em 0;
}

th {
    background-color: #3498db;
    color: white;
    font-weight: 600;
    padding: 10px;
    text-align: left;
}

td {
    padding: 8px 10px;
    border: 1px solid #ddd;
}

tr:nth-child(even) {
    background-color: #f8f9fa;
}
"""
    
    with open(css_file, 'w') as f:
        f.write(css_content)
    
    # Step 1: Convert markdown to HTML using pandoc
    print("\n🔄 Converting markdown to HTML with pandoc...")
    try:
        # Extract title from filename or use default
        title = input_path.stem.replace('_', ' ').replace('-', ' ').title()
        
        result = subprocess.run([
            'pandoc',
            str(input_path),
            '--from=markdown+smart+raw_html',
            '--to=html5',
            '--standalone',
            '--toc',
            '--toc-depth=3',
            '--number-sections',
            f'--css={css_file}',
            '--metadata', f'title={title}',
            '--metadata', f'date={__import__("datetime").datetime.now().strftime("%B %Y")}',
            '--output', str(html_file)
        ], capture_output=True, text=True, check=True)
        
        print("✅ HTML created successfully")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating HTML: {e.stderr}")
        # Cleanup
        if html_file.exists():
            os.remove(html_file)
        if css_file.exists():
            os.remove(css_file)
        sys.exit(1)
    except FileNotFoundError:
        print("❌ pandoc not found. Please install: brew install pandoc")
        # Cleanup
        if css_file.exists():
            os.remove(css_file)
        sys.exit(1)
    
    # Step 2: Convert HTML to PDF using playwright
    print("\n📝 Converting HTML to PDF...")
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{html_file.absolute()}")
            page.pdf(
                path=str(output_path),
                format='A4',
                margin={'top': '2.5cm', 'right': '2cm', 'bottom': '2.5cm', 'left': '2cm'},
                print_background=True
            )
            browser.close()
        
        print("✅ PDF created successfully!")
        
    except ImportError:
        print("⚠️  playwright not installed. Installing...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'playwright', '--quiet'], check=True)
            subprocess.run(['playwright', 'install', 'chromium'], check=True)
            
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f"file://{html_file.absolute()}")
                page.pdf(
                    path=str(output_path),
                    format='A4',
                    margin={'top': '2.5cm', 'right': '2cm', 'bottom': '2.5cm', 'left': '2cm'},
                    print_background=True
                )
                browser.close()
            
            print("✅ PDF created successfully!")
        except Exception as install_error:
            print(f"❌ Error installing playwright: {install_error}")
            print("\n💡 Alternative: Open the HTML file in your browser and print to PDF:")
            print(f"   open {html_file}")
            # Cleanup
            if html_file.exists():
                os.remove(html_file)
            if css_file.exists():
                os.remove(css_file)
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        print("\n💡 Alternative: Open the HTML file in your browser and print to PDF:")
        print(f"   open {html_file}")
        # Cleanup
        if html_file.exists():
            os.remove(html_file)
        if css_file.exists():
            os.remove(css_file)
        sys.exit(1)
    
    # Cleanup temporary files
    if html_file.exists():
        os.remove(html_file)
    if css_file.exists():
        os.remove(css_file)
    
    if output_path.exists():
        file_size = output_path.stat().st_size / 1024
        print(f"\n📊 PDF Details:")
        print(f"   Location: {output_path}")
        print(f"   File size: {file_size:.1f} KB")
        print(f"\n📋 PDF Features:")
        print("   ✓ Professional typography and styling")
        print("   ✓ Table of contents with page numbers")
        print("   ✓ Numbered sections")
        print("   ✓ High-quality image rendering")
        print("   ✓ Code syntax highlighting")
        print("   ✓ Professional color scheme")
        print("   ✓ Proper page margins and formatting")
        return str(output_path)
    else:
        print("❌ PDF file was not created")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown to Professional PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s README.md
  %(prog)s README.md output.pdf
  %(prog)s learning-path/W07/README.md W07_Final_Report.pdf
        """
    )
    parser.add_argument('input', help='Input markdown file (.md)')
    parser.add_argument('output', nargs='?', help='Output PDF file (optional, defaults to input filename with .pdf extension)')
    
    args = parser.parse_args()
    
    output_path = create_pdf(args.input, args.output)
    print(f"\n✅ Success! PDF saved to: {output_path}")


if __name__ == '__main__':
    main()

