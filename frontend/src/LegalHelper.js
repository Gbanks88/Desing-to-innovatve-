import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import InfoIcon from '@mui/icons-material/Info';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const LegalHelper = () => {
  const [terms, setTerms] = useState([]);
  const [selectedTerm, setSelectedTerm] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    fetchTerms();
  }, []);

  const fetchTerms = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/terms`);
      setTerms(response.data.terms);
    } catch (err) {
      setError('Failed to load legal terms');
    }
  };

  const fetchTermDetails = async (term) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/terms/${term}`);
      setSelectedTerm(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load term details');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData);
      setAnalysis(response.data);
      setError(null);
      
      // If we got a document type, fetch its details
      if (response.data.document_type !== 'unknown') {
        await fetchTermDetails(response.data.document_type);
      }
    } catch (err) {
      setError('Failed to analyze document');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, margin: 'auto', p: 2 }}>
      <Alert severity="warning" sx={{ mb: 2 }}>
        <Typography variant="body1" component="div">
          <strong>IMPORTANT LEGAL DISCLAIMER</strong>
          <br />
          This tool is for informational purposes only and is NOT a substitute for professional legal advice.
          Always consult with a qualified attorney for legal matters.
        </Typography>
      </Alert>

      <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6" gutterBottom>
          Document Analysis
        </Typography>
        <Button
          variant="contained"
          component="label"
          startIcon={<UploadFileIcon />}
          sx={{ mb: 2 }}
        >
          Upload Legal Document
          <input
            type="file"
            hidden
            accept=".pdf,.docx"
            onChange={handleFileUpload}
          />
        </Button>

        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
            <CircularProgress />
          </Box>
        )}

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {analysis && (
          <Alert severity="info" sx={{ mb: 2 }}>
            Document Type: {analysis.document_type}
            <br />
            {analysis.disclaimer}
          </Alert>
        )}
      </Paper>

      {selectedTerm && (
        <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Understanding: {selectedTerm.term}
          </Typography>
          <Typography variant="body1" gutterBottom>
            {selectedTerm.info.simple}
          </Typography>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>What to Do</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <List>
                {selectedTerm.info.what_to_do.map((step, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={step} />
                  </ListItem>
                ))}
              </List>
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>Common Questions</Typography>
            </AccordionSummary>
            <AccordionDetails>
              {selectedTerm.info.common_questions.map((qa, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Typography variant="subtitle1" color="primary">
                    Q: {qa.q}
                  </Typography>
                  <Typography variant="body2">
                    A: {qa.a}
                  </Typography>
                  {index < selectedTerm.info.common_questions.length - 1 && (
                    <Divider sx={{ my: 1 }} />
                  )}
                </Box>
              ))}
            </AccordionDetails>
          </Accordion>
        </Paper>
      )}

      <Box sx={{ mt: 2 }}>
        <Typography variant="body2" color="text.secondary" align="center">
          <InfoIcon sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5 }} />
          For immediate legal assistance, contact your local bar association or legal aid society.
        </Typography>
      </Box>
    </Box>
  );
};

export default LegalHelper;
