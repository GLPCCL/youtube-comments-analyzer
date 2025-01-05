import React, { useState } from 'react';
import { TextField, Button, Box, CircularProgress } from '@mui/material';

interface VideoInputProps {
    onAnalyze: (url: string) => Promise<void>;
    isLoading: boolean;
}

const VideoInput: React.FC<VideoInputProps> = ({ onAnalyze, isLoading }) => {
    const [url, setUrl] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (url.trim()) {
            await onAnalyze(url);
        }
    };

    return (
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3, mb: 4 }}>
            <TextField
                fullWidth
                label="URL de la vidéo YouTube"
                variant="outlined"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                disabled={isLoading}
                sx={{ mb: 2 }}
            />
            <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={isLoading || !url.trim()}
                startIcon={isLoading ? <CircularProgress size={20} /> : null}
            >
                {isLoading ? 'Analyse en cours...' : 'Analyser les commentaires'}
            </Button>
        </Box>
    );
};

export default VideoInput;
