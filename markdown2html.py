#!/usr/bin/python3
import sys
import os
import markdown
import re
import hashlib

def convert_markdown_to_html(input_file, output_file):
    try:
        with open(input_file, 'r') as md_file, open(output_file, 'w') as html_file:
            markdown_text = md_file.read()

            # Replace Markdown headings with corresponding HTML headings
            markdown_text = re.sub(r'^#\s(.+)$', r'<h1>\1</h1>', markdown_text, flags=re.MULTILINE)
            markdown_text = re.sub(r'^##\s(.+)$', r'<h2>\1</h2>', markdown_text, flags=re.MULTILINE)
            markdown_text = re.sub(r'^###\s(.+)$', r'<h3>\1</h3>', markdown_text, flags=re.MULTILINE)
            markdown_text = re.sub(r'^####\s(.+)$', r'<h4>\1</h4>', markdown_text, flags=re.MULTILINE)
            markdown_text = re.sub(r'^#####\s(.+)$', r'<h5>\1</h5>', markdown_text, flags=re.MULTILINE)
            markdown_text = re.sub(r'^######\s(.+)$', r'<h6>\1</h6>', markdown_text, flags=re.MULTILINE)

            # Replace Markdown unordered lists with HTML <ul> and <li> tags
            markdown_text = re.sub(r'^-\s(.+)$', r'<ul>\n<li>\1</li>\n</ul>', markdown_text, flags=re.MULTILINE)

            # Replace Markdown ordered lists with HTML <ol> and <li> tags
            markdown_text = re.sub(r'^\*\s(.+)$', r'<ol>\n<li>\1</li>\n</ol>', markdown_text, flags=re.MULTILINE)

            # Replace Markdown bold with HTML <b> tags
            markdown_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', markdown_text)

            # Replace Markdown emphasized (italic) with HTML <em> tags
            markdown_text = re.sub(r'__(.+?)__', r'<em>\1</em>', markdown_text)

            # Process custom syntax: [[Hello]] to MD5 hash (lowercase)
            markdown_text = re.sub(r'\[\[(.+?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), markdown_text)

            # Process custom syntax: ((Hello Chicago)) to remove 'c' (case insensitive)
            markdown_text = re.sub(r'\(\((.+?)\)\)', lambda match: match.group(1).replace('c', '', -1, re.IGNORECASE), markdown_text)

            # Replace Markdown paragraphs and line breaks with HTML <p> and <br> tags
            markdown_text = re.sub(r'^(?!\s*-)\s*(.+)$', r'<p>\1</p>', markdown_text, flags=re.MULTILINE)
            markdown_text = markdown_text.replace('\n', '<br />')

            # Convert the remaining Markdown to HTML
            html_text = markdown.markdown(markdown_text)
            html_file.write(html_text)
        return True
    except FileNotFoundError:
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    success = convert_markdown_to_html(input_file, output_file)
    
    if success:
        sys.exit(0)
    else:
        print(f"Failed to read or write files.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
