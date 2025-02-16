#!/usr/bin/env python3
import os
import sys
import PyPDF2
from datetime import datetime
from pathlib import Path
from legal_terms_helper import LegalTermsExplainer

class LegalResponseHelper:
    def __init__(self):
        self.responses = {}
        self.document_type = None
        self.terms_helper = LegalTermsExplainer()
        self.guidance = {
            "summons": {
                "explanation": """A summons is a legal document that notifies you that a lawsuit has been filed against you. 
                You must respond within the specified time period (usually 20-30 days) or the other party may win by default.""",
                "steps": [
                    "1. Read the summons carefully to understand the deadline to respond",
                    "2. Note the court where the case was filed",
                    "3. Write down the case number",
                    "4. Identify who is suing you (the plaintiff)",
                ],
                "questions": [
                    {
                        "id": "deadline",
                        "question": "What is the deadline to respond (usually found at the top of the summons)?",
                        "help": "Look for text that says 'You have X days to respond' or 'Response required within X days'",
                        "required": True
                    },
                    {
                        "id": "case_number",
                        "question": "What is the case number?",
                        "help": "This is usually at the top of the document, formatted like 'Case No. XXX-XXX'",
                        "required": True
                    },
                    {
                        "id": "court_name",
                        "question": "Which court is handling the case?",
                        "help": "Look for the court name at the top of the document",
                        "required": True
                    },
                    {
                        "id": "plaintiff",
                        "question": "Who is suing you (the plaintiff's name)?",
                        "help": "Look for 'Plaintiff:' or 'vs.' in the document",
                        "required": True
                    },
                    {
                        "id": "claims",
                        "question": "What are they claiming? (Briefly describe the main points)",
                        "help": "Look in the body of the document for what the plaintiff is asking for",
                        "required": True
                    }
                ],
                "response_template": {
                    "header": "RESPONSE TO SUMMONS",
                    "sections": [
                        "RESPONSE TO ALLEGATIONS",
                        "AFFIRMATIVE DEFENSES",
                        "PRAYER FOR RELIEF"
                    ]
                }
            },
            "default_judgment": {
                "explanation": """A default judgment is a decision made by the court when you don't respond to a lawsuit in time. 
                You may be able to ask the court to cancel (vacate) the default judgment if you act quickly and have a good reason.""",
                "questions": [
                    {
                        "id": "judgment_date",
                        "question": "When was the default judgment entered?",
                        "help": "Look for the date the judgment was signed by the judge",
                        "required": True
                    },
                    {
                        "id": "reason_for_default",
                        "question": "Why didn't you respond to the original summons?",
                        "help": "Common reasons: never received it, was ill, family emergency, etc.",
                        "required": True
                    }
                ]
            }
        }

    def start_guided_process(self):
        """Start the guided process for responding to legal documents"""
        print("\n" + "!"*80)
        print("CRITICAL LEGAL NOTICE - PLEASE READ CAREFULLY".center(80))
        print("!"*80)
        print("\nThis tool is NOT a substitute for professional legal representation.")
        print("It is STRONGLY RECOMMENDED that you:")
        print("1. Seek immediate legal representation from a qualified attorney")
        print("2. Contact your local legal aid society if you cannot afford an attorney")
        print("3. Visit your court's self-help center for guidance")
        print("4. Call your local bar association for attorney referrals")
        print("\nFAILURE TO OBTAIN PROPER LEGAL REPRESENTATION MAY RESULT IN:")
        print("- Loss of important legal rights")
        print("- Adverse court judgments")
        print("- Financial consequences")
        print("- Other serious legal implications")
        print("\n" + "!"*80)
        
        input("\nPress Enter to acknowledge this notice...")
        
        print("\nWelcome to the Legal Document Response Helper!")
        print("While this tool can help you understand legal documents better,")
        print("it should NOT be your only resource. Always seek professional legal advice.")
        
        input("\nPress Enter to continue...")
        
        print("\nBefore we begin, have you tried to:")
        print("1. Contact a lawyer or legal aid society?")
        print("2. Visit your court's self-help center?")
        print("3. Call your local bar association?")
        
        response = input("\nHave you attempted any of the above? (yes/no): ").strip().lower()
        if response != 'yes':
            print("\nSTRONGLY RECOMMENDED: Please try these resources first.")
            print("They can provide proper legal guidance for your specific situation.")
            print("Would you like to continue anyway? (This is not recommended)")
            proceed = input("Continue? (yes/no): ").strip().lower()
            if proceed != 'yes':
                print("\nGood decision. Please seek proper legal help first.")
                sys.exit(0)
            
        print("\nFirst, let's understand some basic things:")
        print("1. Every legal document has deadlines - we'll help you find them")
        print("2. You have the right to respond to legal documents")
        print("3. You can ask for help from the court's self-help center")
        print("\nREMINDER: This tool is for information only. Always seek")
        print("professional legal advice for your specific situation.")
        
        input("\nPress Enter to continue...")
        
        # Offer to explain legal terms
        print("\nWould you like to understand any legal terms before we start?")
        print("You can ask about terms like 'summons', 'complaint', or 'default judgment'")
        while True:
            term = input("\nEnter a legal term (or 'continue' to proceed): ").strip().lower()
            if term == 'continue':
                break
            self.terms_helper.explain_term(term)
            print("\nREMINDER: These explanations are simplified for general understanding.")
            print("Consult a legal professional for specific advice about your situation.")

    def identify_document_type(self, pdf_path):
        """Analyze the document and help user identify its type"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text().lower()
                
            print("\nLet's figure out what kind of document you received.")
            print("I'll ask you some simple questions about it.")
            
            if "summons" in text:
                print("\nI see this might be a 'summons' - a document telling you")
                print("that someone is suing you. Let me explain what this means.")
                self.terms_helper.explain_term("summons")
                return "summons"
            
            elif "default judgment" in text:
                print("\nThis looks like a 'default judgment' - a decision made")
                print("because someone didn't respond to a lawsuit in time.")
                self.terms_helper.explain_term("default_judgment")
                return "default_judgment"
            
            # If automated detection fails, ask the user
            print("\nI'm not sure what type of document this is.")
            print("Let's figure it out together.")
            print("\nDo you see any of these words at the top of the document?")
            print("1. Summons")
            print("2. Complaint")
            print("3. Default Judgment")
            print("4. Other/Not Sure")
            
            choice = input("\nEnter the number (1-4): ").strip()
            if choice == "1":
                return "summons"
            elif choice == "2":
                return "complaint"
            elif choice == "3":
                return "default_judgment"
            else:
                print("\nSince we're not sure what type of document this is,")
                print("it would be best to show it to the court's self-help center.")
                print("They can help you understand what it is and what to do next.")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error reading the document: {e}")
            print("Please make sure the file is a valid PDF and try again.")
            sys.exit(1)

    def get_user_responses(self):
        """Guide the user through responding to the document"""
        print("\nI'll help you create your response step by step.")
        print("Take your time and answer each question carefully.")
        print("If you're not sure about something, it's okay to say so.")
        
        for question in self.guidance[self.document_type]["questions"]:
            while True:
                print(f"\n{question['question']}")
                print(f"Help: {question['help']}")
                
                # Offer examples if available
                if "examples" in question:
                    print("\nExamples:")
                    for example in question["examples"]:
                        print(f"- {example}")
                
                answer = input("\nYour answer: ").strip()
                
                if question['required'] and not answer:
                    print("\nThis information is important for your response.")
                    print("Please try to provide an answer.")
                    continue
                
                # Confirm the answer
                print(f"\nYou entered: {answer}")
                confirm = input("Is this correct? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    self.responses[question['id']] = answer
                    break
                print("\nOkay, let's try again.")

    def generate_response_document(self):
        """Generate appropriate legal response based on document type and user inputs"""
        if self.document_type == "summons":
            return self.generate_summons_response()
        elif self.document_type == "default_judgment":
            return self.generate_default_judgment_response()
        return None

    def generate_summons_response(self):
        """Generate response to summons"""
        tex_content = f"""
\\documentclass[12pt,letterpaper]{{article}}
\\usepackage{{document_style}}
\\usepackage{{court_document_integration}}

\\begin{{document}}

\\begin{{center}}
\\textbf{{IN THE {self.responses['court_name'].upper()}}}\\\\
\\vspace{{1em}}
Case No. {self.responses['case_number']}
\\end{{center}}

\\begin{{tabular}}{{l}}
{self.responses['plaintiff']}\\\\
Plaintiff,\\\\
vs.\\\\
{self.get_user_info()}\\\\
Defendant.
\\end{{tabular}}

\\vspace{{2em}}

\\begin{{center}}
\\textbf{{DEFENDANT'S RESPONSE TO SUMMONS}}
\\end{{center}}

\\vspace{{1em}}

COMES NOW the Defendant, and in response to the Plaintiff's Summons and Complaint states:

\\begin{{enumerate}}
    \\item Defendant admits/denies the allegations in paragraph 1...
    [Response to each allegation will be guided through the interface]
\\end{{enumerate}}

\\vspace{{2em}}

\\begin{{center}}
\\textbf{{AFFIRMATIVE DEFENSES}}
\\end{{center}}

[Will be populated based on user responses]

\\vspace{{2em}}

\\begin{{center}}
\\textbf{{PRAYER FOR RELIEF}}
\\end{{center}}

WHEREFORE, Defendant prays that:
\\begin{{enumerate}}
    \\item The Complaint be dismissed;
    \\item Defendant be awarded costs and fees;
    \\item Such other relief as the Court deems just and proper.
\\end{{enumerate}}

\\vspace{{2em}}

Respectfully submitted this {datetime.now().strftime('%d')} day of {datetime.now().strftime('%B, %Y')}.

\\vspace{{2em}}

\\begin{{tabular}}{{l}}
{self.get_user_info()}\\\\
Defendant, Pro Se
\\end{{tabular}}

\\end{{document}}
"""
        return tex_content

    def get_user_info(self):
        """Get user's contact information"""
        if 'user_info' not in self.responses:
            print("\nWe need your contact information for the response:")
            self.responses['user_info'] = {
                'name': input("Your full name: "),
                'address': input("Your address: "),
                'phone': input("Your phone number: "),
                'email': input("Your email address: ")
            }
        
        info = self.responses['user_info']
        return f"{info['name']}\\\\{info['address']}\\\\{info['phone']}\\\\{info['email']}"

    def save_response(self, content):
        """Save the response document"""
        output_path = f"legal_response_{datetime.now().strftime('%Y%m%d')}.tex"
        with open(output_path, 'w') as f:
            f.write(content)
        return output_path

    def main(self):
        if len(sys.argv) != 2:
            print("Usage: python legal_response_helper.py <legal_document.pdf>")
            sys.exit(1)

        # Start the guided process
        self.start_guided_process()
        
        # Identify document type
        doc_type = self.identify_document_type(sys.argv[1])
        if not doc_type:
            print("\nUnable to identify document type.")
            print("IMPORTANT: Please seek immediate legal assistance.")
            print("This could be a complex legal matter requiring professional help.")
            sys.exit(1)
        
        self.document_type = doc_type
        
        # Guide user through response
        self.get_user_responses()
        
        # Generate response document
        response_content = self.generate_response_document()
        
        # Save response
        output_path = self.save_response(response_content)
        print(f"\nI've created your response document: {output_path}")
        print("\nCRITICAL NEXT STEPS:")
        print("1. DO NOT file this document without legal review")
        print("2. Take this document to a lawyer or legal aid society")
        print("3. Visit your court's self-help center for review")
        print("4. Make copies only after professional review")
        print("5. Ask the court clerk about proper filing procedures")
        print("\nFINAL REMINDER: This document is a draft only.")
        print("Always have a legal professional review any court documents")
        print("before filing them. Your legal rights may be affected.")

if __name__ == "__main__":
    helper = LegalResponseHelper()
    helper.main()
