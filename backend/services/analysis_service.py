from transformers import pipeline
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class AnalysisService:
    def __init__(self):
        # Téléchargement des ressources NLTK nécessaires
        nltk.download('punkt')
        nltk.download('stopwords')
        
        # Initialisation du pipeline de sentiment analysis
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
        self.stop_words = set(stopwords.words('french') + stopwords.words('english'))

    def analyze_comments(self, comments):
        """Analyse les commentaires et les classe en catégories."""
        results = {
            'positifs': [],
            'negatifs': [],
            'interrogatifs': [],
            'keywords': {},
            'summary': {}
        }

        for comment in comments:
            # Analyse du sentiment
            sentiment = self._analyze_sentiment(comment['text'])
            
            # Classification du commentaire
            category = self._classify_comment(comment['text'], sentiment)
            
            # Ajout du commentaire à sa catégorie
            comment_data = {
                'text': comment['text'],
                'author': comment['author'],
                'date': comment['date'],
                'sentiment_score': sentiment
            }
            results[category].append(comment_data)

        # Extraction des mots-clés pour chaque catégorie
        for category in ['positifs', 'negatifs', 'interrogatifs']:
            results['keywords'][category] = self._extract_keywords(
                [c['text'] for c in results[category]]
            )

        # Génération des résumés
        results['summary'] = self._generate_summaries(results)

        return results

    def _analyze_sentiment(self, text):
        """Analyse le sentiment d'un texte."""
        try:
            result = self.sentiment_analyzer(text)[0]
            # Conversion du score en échelle -1 à 1
            score = (int(result['label'][0]) - 3) / 2
            return score
        except:
            return 0

    def _classify_comment(self, text, sentiment):
        """Classifie un commentaire en fonction de son contenu et sentiment."""
        text = text.lower()
        
        # Détection des questions
        if '?' in text or any(word in text for word in ['comment', 'pourquoi', 'quand', 'où']):
            return 'interrogatifs'
        
        # Classification basée sur le sentiment
        if sentiment > 0.2:
            return 'positifs'
        elif sentiment < -0.2:
            return 'negatifs'
        else:
            return 'interrogatifs'  # Par défaut si incertain

    def _extract_keywords(self, texts, top_n=10):
        """Extrait les mots-clés les plus fréquents d'une liste de textes."""
        words = []
        for text in texts:
            tokens = word_tokenize(text.lower())
            words.extend([
                word for word in tokens 
                if word.isalnum() and 
                word not in self.stop_words and 
                len(word) > 2
            ])
        
        return dict(Counter(words).most_common(top_n))

    def _generate_summaries(self, results):
        """Génère des résumés pour chaque catégorie."""
        summaries = {}
        for category in ['positifs', 'negatifs', 'interrogatifs']:
            if results[category]:
                keywords = results['keywords'][category]
                count = len(results[category])
                
                if category == 'positifs':
                    summary = f"Il y a {count} commentaires positifs. "
                    summary += f"Les aspects les plus appréciés concernent: {', '.join(list(keywords.keys())[:3])}."
                elif category == 'negatifs':
                    summary = f"Il y a {count} commentaires négatifs. "
                    summary += f"Les principaux points de critique sont: {', '.join(list(keywords.keys())[:3])}."
                else:
                    summary = f"Il y a {count} commentaires interrogatifs. "
                    summary += f"Les questions portent principalement sur: {', '.join(list(keywords.keys())[:3])}."
                
                summaries[category] = summary
                
        return summaries

    def generate_suggestions(self, analysis_results):
        """Génère des suggestions basées sur l'analyse des commentaires."""
        suggestions = []
        
        # Analyse des questions fréquentes
        if analysis_results['interrogatifs']:
            keywords = analysis_results['keywords']['interrogatifs']
            for keyword, count in keywords.items():
                if count >= 3:  # Seuil arbitraire
                    suggestions.append({
                        'type': 'tutoriel',
                        'sujet': keyword,
                        'priorité': count
                    })

        # Analyse des problèmes signalés
        if analysis_results['negatifs']:
            keywords = analysis_results['keywords']['negatifs']
            for keyword, count in keywords.items():
                if count >= 3:
                    suggestions.append({
                        'type': 'amélioration',
                        'sujet': keyword,
                        'priorité': count
                    })

        return suggestions
