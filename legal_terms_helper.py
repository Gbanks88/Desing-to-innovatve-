#!/usr/bin/env python3

class LegalTermsExplainer:
    def __init__(self):
        self.legal_terms = {
            "summons": {
                "simple": "Official notice that someone is suing you",
                "what_to_do": [
                    "Read the whole document carefully",
                    "Note the deadline to respond (usually 20-30 days)",
                    "Write down the case number",
                    "Save all papers you received"
                ],
                "common_questions": [
                    {
                        "q": "What happens if I ignore it?",
                        "a": "If you ignore a summons, you might lose the case automatically (called a 'default judgment'). The other party could then take actions like garnishing your wages or putting a lien on your property."
                    },
                    {
                        "q": "Do I need a lawyer?",
                        "a": "While having a lawyer is helpful, you can represent yourself. Many courts have free legal help centers or self-help resources available."
                    }
                ]
            },
            "complaint": {
                "simple": "Document explaining why someone is suing you",
                "what_to_do": [
                    "Read each numbered paragraph carefully",
                    "Mark which statements you agree or disagree with",
                    "Take notes on anything that's incorrect",
                    "Gather any documents that support your side"
                ],
                "common_questions": [
                    {
                        "q": "What if some statements are partly true?",
                        "a": "You can 'admit in part and deny in part' and then explain what parts are true and false."
                    }
                ]
            },
            "default_judgment": {
                "simple": "Court decision made when you didn't respond in time",
                "what_to_do": [
                    "Act quickly - there are deadlines to challenge it",
                    "Write down why you couldn't respond earlier",
                    "Gather proof of your reason (like medical records)",
                    "Consider seeking legal help immediately"
                ],
                "common_questions": [
                    {
                        "q": "Can I get rid of a default judgment?",
                        "a": "Yes, but you must act quickly and have a good reason for not responding earlier. This is called 'vacating' or 'setting aside' the default judgment."
                    }
                ]
            },
            "answer": {
                "simple": "Your written response to the complaint",
                "what_to_do": [
                    "Respond to each numbered paragraph in the complaint",
                    "Only admit things you're sure are true",
                    "Include any defenses you have",
                    "File within the deadline"
                ],
                "common_questions": [
                    {
                        "q": "What if I'm not sure about something?",
                        "a": "You can say you 'lack sufficient information to admit or deny' that statement."
                    }
                ]
            },
            "service": {
                "simple": "Official delivery of legal papers",
                "what_to_do": [
                    "Keep all papers you receive",
                    "Note how and when you received them",
                    "Don't refuse to accept service",
                    "Read everything immediately"
                ],
                "common_questions": [
                    {
                        "q": "What if I never received the papers?",
                        "a": "If you weren't properly served, you might be able to challenge the case. Document how you found out about the lawsuit."
                    }
                ]
            }
        }

    def explain_term(self, term):
        """Explain a legal term in simple language"""
        term = term.lower()
        if term in self.legal_terms:
            info = self.legal_terms[term]
            print(f"\n{term.upper()}")
            print(f"Simple explanation: {info['simple']}")
            print("\nWhat you should do:")
            for step in info['what_to_do']:
                print(f"- {step}")
            print("\nCommon questions:")
            for qa in info['common_questions']:
                print(f"\nQ: {qa['q']}")
                print(f"A: {qa['a']}")
            return True
        return False

    def get_term_suggestions(self, partial_term):
        """Get suggestions for partial terms"""
        partial_term = partial_term.lower()
        return [term for term in self.legal_terms.keys() 
                if partial_term in term]

    def interactive_help(self):
        """Provide interactive help for legal terms"""
        print("\n" + "*"*80)
        print("IMPORTANT LEGAL DISCLAIMER".center(80))
        print("This tool is for informational purposes only and is NOT a substitute")
        print("for professional legal advice. You should ALWAYS:")
        print("1. Seek advice from a qualified attorney for your specific situation")
        print("2. Consult with legal aid or a pro bono legal service if you cannot afford an attorney")
        print("3. Contact your local bar association for referrals to qualified attorneys")
        print("4. Never rely solely on this tool for legal decisions")
        print("*"*80 + "\n")
        
        print("Welcome to the Legal Terms Helper!")
        print("This tool helps explain legal terms in simple language.")
        print("Remember: This is just a guide to help you understand terms better.")
        print("Always consult with a legal professional for actual legal advice.")
        print("\nType 'quit' to exit, 'list' to see all terms, or enter a legal term to learn about it.")
        
        while True:
            term = input("\nWhat legal term would you like to understand? ").strip().lower()
            
            if term == 'quit':
                print("\nRemember: Always seek professional legal advice for your specific situation.")
                break
            elif term == 'list':
                print("\nAvailable terms:")
                for available_term in self.legal_terms.keys():
                    print(f"- {available_term}")
                continue
            
            if not self.explain_term(term):
                suggestions = self.get_term_suggestions(term)
                if suggestions:
                    print("\nTerm not found. Did you mean one of these?")
                    for suggestion in suggestions:
                        print(f"- {suggestion}")
                else:
                    print("\nTerm not found. Type 'list' to see all available terms.")
            
            print("\nREMINDER: This explanation is for general understanding only.")
            print("Consult a legal professional for advice about your specific situation.")

def main():
    helper = LegalTermsExplainer()
    helper.interactive_help()

if __name__ == "__main__":
    main()
