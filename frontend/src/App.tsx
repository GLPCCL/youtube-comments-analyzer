import React, { useState } from 'react';
import { TextField, Button, Container, Typography, Box, CircularProgress } from '@mui/material';
import './App.css';

type AnalysisResult = {
  sentiment: {
    positive: number;
    negative: number;
    neutral: number;
  };
  keywords: string[];
  suggestions: string[];
}

const App: React.FC = () => {
  const [videoUrl, setVideoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_url: videoUrl }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze video');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          YouTube Comments Analyzer
        </Typography>

        <Box sx={{ my: 2 }}>
          <TextField
            fullWidth
            label="YouTube Video URL"
            variant="outlined"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
            disabled={loading}
          />
        </Box>

        <Button
          variant="contained"
          onClick={handleAnalyze}
          disabled={!videoUrl || loading}
          sx={{ my: 2 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Analyze Comments'}
        </Button>

        {error && (
          <Typography color="error" sx={{ my: 2 }}>
            {error}
          </Typography>
        )}

        {result && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom>
              Analysis Results
            </Typography>
            
            <Typography variant="h6" gutterBottom>
              Sentiment Distribution
            </Typography>
            <Typography>
              Positive: {(result.sentiment.positive * 100).toFixed(1)}%
              <br />
              Negative: {(result.sentiment.negative * 100).toFixed(1)}%
              <br />
              Neutral: {(result.sentiment.neutral * 100).toFixed(1)}%
            </Typography>

            <Typography variant="h6" sx={{ mt: 2 }} gutterBottom>
              Key Topics
            </Typography>
            <Typography>
              {result.keywords.join(', ')}
            </Typography>

            <Typography variant="h6" sx={{ mt: 2 }} gutterBottom>
              Content Suggestions
            </Typography>
            <Typography>
              {result.suggestions.map((suggestion, index) => (
                <div key={index}>{suggestion}</div>
              ))}
            </Typography>
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default App;
