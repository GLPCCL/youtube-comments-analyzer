from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from backend.services.youtube_service import YouTubeService
from backend.services.analysis_service import AnalysisService
from backend.services.visualization_service import VisualizationService

load_dotenv()

app = Flask(__name__)
CORS(app)

youtube_service = YouTubeService(os.getenv('YOUTUBE_API_KEY'))
analysis_service = AnalysisService()
visualization_service = VisualizationService()

@app.route('/api/quota', methods=['GET'])
def get_quota():
    """Retourne le quota restant pour aujourd'hui"""
    try:
        remaining_quota = youtube_service.quota_manager.get_remaining_quota()
        return jsonify({
            'remaining_quota': remaining_quota,
            'max_quota': youtube_service.quota_manager.MAX_DAILY_QUOTA
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_comments():
    """Analyse les commentaires d'une vidéo YouTube"""
    video_url = request.json.get('video_url')
    if not video_url:
        return jsonify({'error': 'URL de vidéo manquante'}), 400

    try:
        # Extraction des commentaires
        comments = youtube_service.get_video_comments(video_url)
        
        # Analyse des commentaires
        analysis_results = analysis_service.analyze_comments(comments)
        
        # Génération des visualisations
        visualizations = visualization_service.generate_visualizations(analysis_results)
        
        # Génération des suggestions
        suggestions = analysis_service.generate_suggestions(analysis_results)
        
        return jsonify({
            'analysis': analysis_results,
            'visualizations': visualizations,
            'suggestions': suggestions,
            'quota_remaining': youtube_service.quota_manager.get_remaining_quota()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
