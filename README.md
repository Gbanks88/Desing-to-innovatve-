# Legal Document Helper Widget

A web-based legal document helper that can be integrated into any website. This tool helps users understand legal documents while consistently emphasizing the importance of seeking professional legal advice.

## Important Disclaimer

This tool is for informational purposes only and is NOT a substitute for professional legal advice. Always consult with a qualified attorney for legal matters.

## Features

- Document type analysis
- Legal term explanations
- Step-by-step guidance
- Common questions and answers
- Professional advice recommendations
- Modern, responsive UI
- Strong emphasis on seeking legal counsel

## Technical Stack

### Backend (Flask API)
- Python 3.7+
- Flask
- PyPDF2 for document analysis
- CORS support
- File upload handling

### Frontend (React Component)
- React 18
- Material-UI components
- Axios for API calls
- Responsive design
- Accessibility features

## Installation

### Backend Setup
1. Navigate to the api directory:
```bash
cd api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the server:
```bash
python app.py
```

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## Integration

To add this widget to your website:

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Add the component to your React application:
```jsx
import LegalHelper from './components/LegalHelper';

function App() {
  return (
    <div>
      <LegalHelper />
    </div>
  );
}
```

3. Configure the API endpoint:
```bash
# In your .env file
REACT_APP_API_URL=http://your-api-domain/api
```

## Security Considerations

- All uploaded files are temporarily stored and immediately deleted after analysis
- No sensitive information is stored
- CORS is properly configured
- Input validation and sanitization implemented
- Secure file handling

## Legal Compliance

This tool:
- Does NOT provide legal advice
- Consistently emphasizes the need for professional legal counsel
- Includes clear disclaimers
- Encourages users to seek proper legal assistance
- Provides resources for finding legal help

## Support

For technical support with integration, please open an issue in the repository.

For legal matters, always consult with a qualified attorney or legal aid society.
