import json
from datetime import datetime, date
import os

class QuotaManager:
    def __init__(self, quota_file="quota_usage.json"):
        self.quota_file = quota_file
        self.MAX_DAILY_QUOTA = 10000
        self.load_quota_usage()

    def load_quota_usage(self):
        """Charge l'utilisation du quota depuis le fichier"""
        if os.path.exists(self.quota_file):
            with open(self.quota_file, 'r') as f:
                data = json.load(f)
                if data['date'] == str(date.today()):
                    self.daily_usage = data['usage']
                else:
                    self.daily_usage = 0
        else:
            self.daily_usage = 0

    def save_quota_usage(self):
        """Sauvegarde l'utilisation du quota dans le fichier"""
        with open(self.quota_file, 'w') as f:
            json.dump({
                'date': str(date.today()),
                'usage': self.daily_usage
            }, f)

    def can_make_request(self, cost=1):
        """Vérifie si une requête peut être effectuée"""
        return (self.daily_usage + cost) <= self.MAX_DAILY_QUOTA

    def add_usage(self, cost=1):
        """Ajoute l'utilisation du quota"""
        if not self.can_make_request(cost):
            raise Exception("Quota journalier dépassé")
        self.daily_usage += cost
        self.save_quota_usage()

    def get_remaining_quota(self):
        """Retourne le quota restant"""
        return self.MAX_DAILY_QUOTA - self.daily_usage
