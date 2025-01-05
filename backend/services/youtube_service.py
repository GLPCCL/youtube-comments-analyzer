from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

class YouTubeService:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)

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
        """Récupère tous les commentaires d'une vidéo YouTube."""
        video_id = self.extract_video_id(video_url)
        comments = []
        
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                textFormat="plainText"
            )

            while request:
                response = request.execute()
                
                for item in response["items"]:
                    comment = item["snippet"]["topLevelComment"]["snippet"]
                    comments.append({
                        'text': comment["textDisplay"],
                        'author': comment["authorDisplayName"],
                        'date': comment["publishedAt"],
                        'likes': comment["likeCount"]
                    })

                request = self.youtube.commentThreads().list_next(request, response)
                
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des commentaires: {str(e)}")

        return comments
