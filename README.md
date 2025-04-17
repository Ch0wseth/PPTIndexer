# PPTIndexer

PPTIndexer est un projet conçu pour extraire, convertir et indexer le contenu de fichiers PowerPoint (PPT/PPTX) dans Azure AI Search. Ce pipeline permet de transformer les diapositives en texte structuré (Markdown), de générer des vecteurs d'embedding pour la recherche sémantique et d'indexer les données dans un moteur de recherche.

## Fonctionnalités

- **Conversion de fichiers PowerPoint en PDF** : Les fichiers PPT/PPTX sont convertis en PDF pour un traitement ultérieur.
- **Extraction d'images des diapositives** : Les pages des PDF sont extraites sous forme d'images.
- **Conversion des images en Markdown** : Utilisation de modèles GPT pour extraire le contenu des images et le convertir en texte Markdown.
- **Génération d'embeddings** : Création de vecteurs d'embedding à l'aide d'Azure OpenAI pour une recherche sémantique avancée.
- **Indexation dans Azure AI Search** : Les données sont indexées dans Azure AI Search pour permettre des recherches rapides et efficaces.

## Structure du projet

- **`front/`** : Contient l'interface utilisateur pour télécharger les fichiers.
  - `index.html` : Interface web permettant de glisser-déposer ou de sélectionner des fichiers pour les envoyer au backend.
- **`backend/`** : Contient les scripts Python pour le traitement des fichiers et l'indexation.
  - `indexation.py` : Script principal pour orchestrer le pipeline d'extraction et d'indexation.
  - `doc2md_utils.py` : Utilitaires pour la conversion, l'extraction et l'indexation.
  - `schema.json` : Définition du schéma d'indexation pour Azure AI Search.
  - `config.json` : Fichier de configuration pour les clés et paramètres Azure.
- **`README.md`** : Documentation du projet.

## Prérequis

- Python 3.8 ou supérieur
- Azure Blob Storage
- Azure AI Search
- Azure OpenAI
- Bibliothèques Python nécessaires (voir `requirements.txt`)

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/PPTIndexer.git
   cd PPTIndexer

# Code adapté de GPT4oContentExtraction (https://github.com/liamca/GPT4oContentExtraction)