import React from 'react';
import {
    Box,
    Paper,
    Typography,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Chip,
} from '@mui/material';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';
import BuildIcon from '@mui/icons-material/Build';
import { Suggestion } from '../types/types';

interface SuggestionsProps {
    suggestions: Suggestion[];
}

const Suggestions: React.FC<SuggestionsProps> = ({ suggestions }) => {
    return (
        <Box sx={{ mt: 4 }}>
            <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                    Suggestions de Contenu
                </Typography>
                <List>
                    {suggestions.map((suggestion, index) => (
                        <ListItem key={index}>
                            <ListItemIcon>
                                {suggestion.type === 'tutoriel' ? (
                                    <VideoLibraryIcon color="primary" />
                                ) : (
                                    <BuildIcon color="secondary" />
                                )}
                            </ListItemIcon>
                            <ListItemText
                                primary={suggestion.sujet}
                                secondary={`Type: ${suggestion.type}`}
                            />
                            <Chip
                                label={`Priorité: ${suggestion.priorité}`}
                                color={suggestion.priorité > 5 ? 'error' : 'default'}
                                size="small"
                            />
                        </ListItem>
                    ))}
                </List>
            </Paper>
        </Box>
    );
};

export default Suggestions;
