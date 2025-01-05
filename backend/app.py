from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from services.youtube_service import YouTubeService
from services.analysis_service import AnalysisService
from services.visualization_service import VisualizationService

load_dotenv()

app = Flask(__name__)
CORS(app)

youtube_service = YouTubeService(os.getenv('YOUTUBE_API_KEY'))
analysis_service = AnalysisService()
visualization_service = VisualizationService()

@app.route('/api/analyze', methods=['POST'])
def analyze_comments():
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
            'suggestions': suggestions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
