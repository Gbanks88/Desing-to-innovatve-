#!/usr/bin/env python3
import os
import sys
import docx
import PyPDF2
import re
from pathlib import Path
import json

class DocumentConverter:
    def __init__(self):
        self.field_mappings = {
            "name": r"(?i)name:\s*(.*)",
            "address": r"(?i)address:\s*(.*)",
            "phone": r"(?i)phone:\s*(.*)",
            "email": r"(?i)email:\s*(.*)",
            "case_number": r"(?i)case\s*(?:no|number|#)?\s*:\s*(.*)",
            "court": r"(?i)court:\s*(.*)",
            "division": r"(?i)division:\s*(.*)",
            "statement": r"(?i)statement:\s*(.*)",
            "declaration": r"(?i)(?:I|1)\s*,\s*(.*?)\s*,\s*declare",
        }

    def extract_from_pdf(self, pdf_path):
        """Extract text and form fields from PDF"""
        data = {}
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # Extract form fields if present
                if pdf_reader.get_fields():
                    for field, value in pdf_reader.get_fields().items():
                        data[field] = value

                # Extract information using regex patterns
                for field, pattern in self.field_mappings.items():
                    match = re.search(pattern, text)
                    if match and field not in data:
                        data[field] = match.group(1).strip()

        except Exception as e:
            print(f"Error processing PDF: {e}")
        return data

    def extract_from_docx(self, docx_path):
        """Extract text and form fields from Word document"""
        data = {}
        try:
            doc = docx.Document(docx_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            # Extract information using regex patterns
            for field, pattern in self.field_mappings.items():
                match = re.search(pattern, text)
                if match:
                    data[field] = match.group(1).strip()

        except Exception as e:
            print(f"Error processing Word document: {e}")
        return data

    def generate_tex_content(self, data):
        """Generate LaTeX content from extracted data"""
        tex_template = r"""
\documentclass[12pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage{document_style}
\usepackage{court_document_integration}

\begin{document}

\thispagestyle{firstpage}

% Case Information
\begin{caseinfo}
%(case_info)s
\end{caseinfo}

\vspace{1em}

% Party Information
\begin{partyinfo}{Party}
%(party_info)s
\end{partyinfo}

\vspace{2em}

% Main Document Content
\begin{courtdocument}{DECLARATION}
%(declaration)s
\end{courtdocument}

\vspace{2em}

% Verification
\begin{verification}
\end{verification}

\end{document}
"""
        # Format case information
        case_info = f"""
\\courtformfield{{casenumber}}{{{data.get('case_number', '')}}}
\\courtformfield{{court}}{{{data.get('court', '')}}}
\\courtformfield{{division}}{{{data.get('division', '')}}}
"""

        # Format party information
        party_info = f"""
\\courtformfield{{name}}{{{data.get('name', '')}}}
\\courtformfield{{address}}{{{data.get('address', '')}}}
\\courtformfield{{phone}}{{{data.get('phone', '')}}}
\\courtformfield{{email}}{{{data.get('email', '')}}}
"""

        # Format declaration
        declaration = f"""
I, {data.get('name', '\\courtformfield{declarantName}{Enter your full name}')}, declare as follows:

\\begin{{enumerate}}
    \\item {data.get('statement', '\\courtformfield{statement1}{Enter your statement here}')}
\\end{{enumerate}}
"""

        return tex_template % {
            'case_info': case_info,
            'party_info': party_info,
            'declaration': declaration
        }

    def convert_document(self, input_path):
        """Convert document and generate LaTeX output"""
        # Determine file type and extract data
        if input_path.lower().endswith('.pdf'):
            data = self.extract_from_pdf(input_path)
        elif input_path.lower().endswith(('.docx', '.doc')):
            data = self.extract_from_docx(input_path)
        else:
            raise ValueError("Unsupported file format")

        # Generate LaTeX content
        tex_content = self.generate_tex_content(data)
        
        # Save the LaTeX file
        output_path = Path(input_path).with_suffix('.tex')
        with open(output_path, 'w') as f:
            f.write(tex_content)
        
        return output_path

def main():
    if len(sys.argv) != 2:
        print("Usage: python document_converter.py <input_file>")
        sys.exit(1)

    converter = DocumentConverter()
    try:
        output_path = converter.convert_document(sys.argv[1])
        print(f"Successfully converted document to: {output_path}")
    except Exception as e:
        print(f"Error converting document: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
