from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import PyPDF2
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class LegalTermsService:
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
            # Add more terms as needed
        }

    def get_term_info(self, term):
        return self.legal_terms.get(term.lower())

    def get_all_terms(self):
        return list(self.legal_terms.keys())

legal_service = LegalTermsService()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/terms', methods=['GET'])
def get_terms():
    return jsonify({
        "terms": legal_service.get_all_terms(),
        "disclaimer": "This information is for educational purposes only. Always consult with a legal professional."
    })

@app.route('/api/terms/<term>', methods=['GET'])
def get_term_details(term):
    term_info = legal_service.get_term_info(term)
    if term_info:
        return jsonify({
            "term": term,
            "info": term_info,
            "disclaimer": "This information is for educational purposes only. Always consult with a legal professional."
        })
    return jsonify({"error": "Term not found"}), 404

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Basic document analysis
        try:
            doc_type = analyze_document(filepath)
            return jsonify({
                "message": "File uploaded successfully",
                "document_type": doc_type,
                "filename": filename,
                "disclaimer": "This is an automated analysis. Please consult with a legal professional."
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return jsonify({"error": "File type not allowed"}), 400

def analyze_document(filepath):
    """Basic document analysis to determine type"""
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text().lower()
            
            if "summons" in text:
                return "summons"
            elif "complaint" in text:
                return "complaint"
            elif "default judgment" in text:
                return "default_judgment"
            return "unknown"
    except Exception:
        return "unknown"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
