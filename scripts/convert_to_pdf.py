import os
import markdown
from weasyprint import HTML, CSS
from datetime import datetime

def convert_md_to_pdf(input_file, output_file):
    # Read markdown content
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['extra', 'codehilite', 'tables', 'toc']
    )
    
    # Add CSS styling
    css = """
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        margin: 40px;
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    h1 {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }
    h2 {
        color: #34495e;
        margin-top: 30px;
    }
    h3 {
        color: #445566;
    }
    code {
        background-color: #f8f9fa;
        padding: 2px 5px;
        border-radius: 3px;
        font-family: monospace;
    }
    pre {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f5f6fa;
    }
    .date {
        color: #666;
        font-style: italic;
        text-align: right;
        margin-bottom: 20px;
    }
    """
    
    # Create complete HTML document
    complete_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Project Documentation</title>
        <style>{css}</style>
    </head>
    <body>
        <div class="date">Generated on {datetime.now().strftime('%B %d, %Y')}</div>
        {html_content}
    </body>
    </html>
    """
    
    # Convert HTML to PDF
    HTML(string=complete_html).write_pdf(
        output_file,
        stylesheets=[CSS(string=css)]
    )

def convert_all_docs():
    # Create docs/pdf directory if it doesn't exist
    pdf_dir = os.path.join('docs', 'pdf')
    os.makedirs(pdf_dir, exist_ok=True)
    
    # List of markdown files to convert
    md_files = [
        'docs/project_analysis.md',
        'docs/cost_optimization.md',
        'docs/digitalocean_setup.md',
        'docs/dns_setup_guide.md',
        'docs/server_setup_guide.md'
    ]
    
    for md_file in md_files:
        if os.path.exists(md_file):
            # Create PDF filename
            pdf_name = os.path.splitext(os.path.basename(md_file))[0] + '.pdf'
            pdf_path = os.path.join(pdf_dir, pdf_name)
            
            print(f"Converting {md_file} to {pdf_path}...")
            try:
                convert_md_to_pdf(md_file, pdf_path)
                print(f"✓ Successfully converted {pdf_name}")
            except Exception as e:
                print(f"✗ Error converting {md_file}: {str(e)}")

if __name__ == "__main__":
    convert_all_docs()
