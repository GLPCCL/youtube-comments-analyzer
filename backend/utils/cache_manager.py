import json
import os
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, cache_file="comments_cache.json", cache_duration_days=1):
        self.cache_file = cache_file
        self.cache_duration = timedelta(days=cache_duration_days)
        self.load_cache()

    def load_cache(self):
        """Charge le cache depuis le fichier"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def save_cache(self):
        """Sauvegarde le cache dans le fichier"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def get_cached_comments(self, video_id):
        """Récupère les commentaires en cache pour une vidéo"""
        if video_id in self.cache:
            cached_data = self.cache[video_id]
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data['comments']
        return None

    def cache_comments(self, video_id, comments):
        """Met en cache les commentaires d'une vidéo"""
        self.cache[video_id] = {
            'timestamp': datetime.now().isoformat(),
            'comments': comments
        }
        self.save_cache()

    def clear_old_cache(self):
        """Nettoie les entrées de cache expirées"""
        now = datetime.now()
        self.cache = {
            video_id: data
            for video_id, data in self.cache.items()
            if now - datetime.fromisoformat(data['timestamp']) < self.cache_duration
        }
        self.save_cache()
