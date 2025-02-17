import os
from fpdf import FPDF
import markdown
import re
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'John Allen\'s Fashion Platform Documentation', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} - Generated on {datetime.now().strftime("%B %d, %Y")}', 0, 0, 'C')

def convert_md_to_pdf(input_file, output_file):
    # Read markdown content
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(md_content)

    # Create PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add title
    pdf.set_font('Arial', 'B', 16)
    title = os.path.splitext(os.path.basename(input_file))[0].replace('_', ' ').title()
    pdf.cell(0, 10, title, 0, 1, 'C')
    pdf.ln(10)

    # Process content
    pdf.set_font('Arial', '', 11)
    
    # Split content into lines
    lines = html_content.split('\n')
    
    for line in lines:
        # Remove HTML tags
        line = re.sub('<[^<]+?>', '', line).strip()
        
        if not line:
            pdf.ln(5)
            continue
            
        # Handle headers
        if line.startswith('# '):
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, line[2:], 0, 1)
            pdf.set_font('Arial', '', 11)
        elif line.startswith('## '):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, line[3:], 0, 1)
            pdf.set_font('Arial', '', 11)
        elif line.startswith('### '):
            pdf.set_font('Arial', 'BI', 11)
            pdf.cell(0, 10, line[4:], 0, 1)
            pdf.set_font('Arial', '', 11)
        else:
            # Handle code blocks
            if line.startswith('    '):
                pdf.set_font('Courier', '', 10)
                pdf.multi_cell(0, 5, line.strip())
                pdf.set_font('Arial', '', 11)
            else:
                # Handle bullet points
                if line.startswith('- '):
                    pdf.cell(5, 5, '-')
                    pdf.multi_cell(0, 5, line[2:])
                else:
                    pdf.multi_cell(0, 5, line)
        
    pdf.output(output_file, 'F')

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
    
    print("\nConverting documentation to PDF...")
    print("=" * 40)
    
    for md_file in md_files:
        if os.path.exists(md_file):
            # Create PDF filename
            pdf_name = os.path.splitext(os.path.basename(md_file))[0] + '.pdf'
            pdf_path = os.path.join(pdf_dir, pdf_name)
            
            print(f"\nProcessing: {md_file}")
            try:
                convert_md_to_pdf(md_file, pdf_path)
                print(f"[SUCCESS] Created {pdf_path}")
            except Exception as e:
                print(f"[ERROR] Failed: {str(e)}")
    
    print("\nConversion complete!")
    print("=" * 40)
    print(f"PDF files are available in: {os.path.abspath(pdf_dir)}\n")

if __name__ == "__main__":
    convert_all_docs()
