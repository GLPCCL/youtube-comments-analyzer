import plotly.graph_objects as go
import plotly.express as px
import json

class VisualizationService:
    def generate_visualizations(self, analysis_results):
        """Génère les visualisations pour l'analyse des commentaires."""
        visualizations = {
            'distribution': self._create_distribution_chart(analysis_results),
            'keywords': self._create_keywords_chart(analysis_results),
            'timeline': self._create_timeline_chart(analysis_results)
        }
        return visualizations

    def _create_distribution_chart(self, results):
        """Crée un graphique circulaire montrant la distribution des catégories."""
        categories = ['positifs', 'negatifs', 'interrogatifs']
        values = [len(results[cat]) for cat in categories]
        
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=values,
            hole=.3,
            marker_colors=['#2ecc71', '#e74c3c', '#3498db']
        )])
        
        fig.update_layout(
            title="Distribution des Commentaires",
            showlegend=True
        )
        
        return json.loads(fig.to_json())

    def _create_keywords_chart(self, results):
        """Crée un graphique à barres des mots-clés les plus fréquents par catégorie."""
        charts = {}
        colors = {
            'positifs': '#2ecc71',
            'negatifs': '#e74c3c',
            'interrogatifs': '#3498db'
        }
        
        for category in ['positifs', 'negatifs', 'interrogatifs']:
            keywords = results['keywords'][category]
            if keywords:
                fig = go.Figure(data=[go.Bar(
                    x=list(keywords.keys()),
                    y=list(keywords.values()),
                    marker_color=colors[category]
                )])
                
                fig.update_layout(
                    title=f"Mots-clés - {category.capitalize()}",
                    xaxis_title="Mots",
                    yaxis_title="Fréquence"
                )
                
                charts[category] = json.loads(fig.to_json())
        
        return charts

    def _create_timeline_chart(self, results):
        """Crée un graphique temporel montrant l'évolution des commentaires."""
        # Création d'une liste de tous les commentaires avec leur catégorie
        all_comments = []
        for category in ['positifs', 'negatifs', 'interrogatifs']:
            for comment in results[category]:
                all_comments.append({
                    'date': comment['date'],
                    'category': category
                })
        
        # Tri par date
        all_comments.sort(key=lambda x: x['date'])
        
        # Création des données pour le graphique
        dates = [comment['date'] for comment in all_comments]
        categories = [comment['category'] for comment in all_comments]
        
        fig = go.Figure()
        
        for category in ['positifs', 'negatifs', 'interrogatifs']:
            mask = [cat == category for cat in categories]
            fig.add_trace(go.Scatter(
                x=[d for i, d in enumerate(dates) if mask[i]],
                y=[1 for i in range(sum(mask))],
                name=category,
                mode='markers',
                marker=dict(
                    size=10,
                    symbol='circle',
                    color={'positifs': '#2ecc71', 'negatifs': '#e74c3c', 'interrogatifs': '#3498db'}[category]
                )
            ))
        
        fig.update_layout(
            title="Chronologie des Commentaires",
            xaxis_title="Date",
            showlegend=True
        )
        
        return json.loads(fig.to_json())
