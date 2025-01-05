# YouTube Comments Analyzer

Une application d'analyse automatique des commentaires YouTube qui permet de :
- Classer les commentaires en catégories (Positifs, Négatifs, Interrogatifs)
- Générer des résumés des principaux thèmes
- Afficher des visualisations interactives
- Proposer des suggestions de contenu

## Installation

1. Cloner le repository
2. Installer les dépendances Python :
```bash
pip install -r requirements.txt
```
3. Configurer les variables d'environnement :
   - Créer un fichier `.env` à la racine du projet
   - Ajouter votre clé API YouTube : `YOUTUBE_API_KEY=votre_clé_api`

## Structure du Projet

```
youtube-comments-analyzer/
├── backend/
│   ├── api/
│   ├── services/
│   └── utils/
├── frontend/
│   ├── src/
│   └── public/
├── requirements.txt
└── README.md
```

## Utilisation

1. Lancer le serveur backend :
```bash
python backend/app.py
```

2. Lancer le frontend :
```bash
cd frontend
npm start
```

3. Accéder à l'application sur `http://localhost:3000`
