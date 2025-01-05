from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
from ..utils.quota_manager import QuotaManager
from ..utils.cache_manager import CacheManager

class YouTubeService:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.quota_manager = QuotaManager()
        self.cache_manager = CacheManager()
        self.MAX_COMMENTS = 200  # Limite à 200 commentaires par vidéo
        self.COMMENTS_PER_PAGE = 20  # Nombre de commentaires par page d'API

    def extract_video_id(self, url):
        """Extrait l'ID de la vidéo depuis l'URL YouTube."""
        parsed_url = urlparse(url)
        if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query)['v'][0]
        raise ValueError("URL YouTube invalide")

    def get_video_comments(self, video_url):
        """Récupère les commentaires d'une vidéo YouTube avec gestion du quota."""
        video_id = self.extract_video_id(video_url)
        
        # Vérifier le cache
        cached_comments = self.cache_manager.get_cached_comments(video_id)
        if cached_comments:
            return cached_comments

        comments = []
        next_page_token = None
        pages_fetched = 0
        max_pages = self.MAX_COMMENTS // self.COMMENTS_PER_PAGE

        try:
            while pages_fetched < max_pages:
                # Vérifier le quota avant chaque requête
                if not self.quota_manager.can_make_request(cost=1):
                    raise Exception(
                        f"Quota journalier atteint. Réessayez demain. "
                        f"Commentaires récupérés : {len(comments)}"
                    )

                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=self.COMMENTS_PER_PAGE,
                    pageToken=next_page_token,
                    textFormat="plainText"
                )

                response = request.execute()
                self.quota_manager.add_usage(cost=1)

                for item in response["items"]:
                    comment = item["snippet"]["topLevelComment"]["snippet"]
                    comments.append({
                        'text': comment["textDisplay"],
                        'author': comment["authorDisplayName"],
                        'date': comment["publishedAt"],
                        'likes': comment["likeCount"]
                    })

                next_page_token = response.get("nextPageToken")
                pages_fetched += 1

                if not next_page_token:
                    break

            # Mettre en cache les commentaires récupérés
            self.cache_manager.cache_comments(video_id, comments)
            return comments

        except Exception as e:
            quota_remaining = self.quota_manager.get_remaining_quota()
            raise Exception(
                f"Erreur lors de la récupération des commentaires: {str(e)}. "
                f"Quota restant: {quota_remaining} unités"
            )
