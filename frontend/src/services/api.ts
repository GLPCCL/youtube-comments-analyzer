import { ApiResponse } from '../types/types';

const API_URL = 'http://localhost:5000/api';

export const analyzeVideo = async (videoUrl: string): Promise<ApiResponse> => {
    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ video_url: videoUrl }),
        });

        if (!response.ok) {
            throw new Error('Erreur lors de l\'analyse de la vidéo');
        }

        return await response.json();
    } catch (error) {
        console.error('Erreur API:', error);
        throw error;
    }
};
