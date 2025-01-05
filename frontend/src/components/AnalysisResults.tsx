import React from 'react';
import { Box, Paper, Typography, Grid } from '@mui/material';
import Plot from 'react-plotly.js';
import { AnalysisResults as AnalysisResultsType } from '../types/types';

interface AnalysisResultsProps {
    results: AnalysisResultsType;
    visualizations: {
        distribution: any;
        keywords: { [category: string]: any };
        timeline: any;
    };
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results, visualizations }) => {
    return (
        <Box sx={{ mt: 4 }}>
            <Grid container spacing={3}>
                {/* Distribution des commentaires */}
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6" gutterBottom>
                            Distribution des Commentaires
                        </Typography>
                        <Plot
                            data={visualizations.distribution.data}
                            layout={visualizations.distribution.layout}
                            useResizeHandler
                            style={{ width: '100%', height: '400px' }}
                        />
                    </Paper>
                </Grid>

                {/* Mots-clés par catégorie */}
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6" gutterBottom>
                            Mots-clés par Catégorie
                        </Typography>
                        {Object.entries(visualizations.keywords).map(([category, chart]) => (
                            <Box key={category} sx={{ mb: 3 }}>
                                <Typography variant="subtitle1" gutterBottom>
                                    {category.charAt(0).toUpperCase() + category.slice(1)}
                                </Typography>
                                <Plot
                                    data={chart.data}
                                    layout={chart.layout}
                                    useResizeHandler
                                    style={{ width: '100%', height: '200px' }}
                                />
                            </Box>
                        ))}
                    </Paper>
                </Grid>

                {/* Chronologie */}
                <Grid item xs={12}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6" gutterBottom>
                            Chronologie des Commentaires
                        </Typography>
                        <Plot
                            data={visualizations.timeline.data}
                            layout={visualizations.timeline.layout}
                            useResizeHandler
                            style={{ width: '100%', height: '300px' }}
                        />
                    </Paper>
                </Grid>

                {/* Résumés */}
                <Grid item xs={12}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6" gutterBottom>
                            Résumé de l'Analyse
                        </Typography>
                        {Object.entries(results.summary).map(([category, summary]) => (
                            <Typography key={category} paragraph>
                                <strong>{category.charAt(0).toUpperCase() + category.slice(1)}:</strong>{' '}
                                {summary}
                            </Typography>
                        ))}
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default AnalysisResults;
