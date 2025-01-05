import React, { useState } from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme, Alert } from '@mui/material';
import VideoInput from './components/VideoInput';
import AnalysisResults from './components/AnalysisResults';
import Suggestions from './components/Suggestions';
import { analyzeVideo } from './services/api';
import { ApiResponse } from './types/types';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<ApiResponse | null>(null);

  const handleAnalyze = async (url: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyzeVideo(url);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Une erreur est survenue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <h1>Analyseur de Commentaires YouTube</h1>
        
        <VideoInput onAnalyze={handleAnalyze} isLoading={loading} />
        
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
        
        {results && (
          <>
            <AnalysisResults
              results={results.analysis}
              visualizations={results.visualizations}
            />
            <Suggestions suggestions={results.suggestions} />
          </>
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
