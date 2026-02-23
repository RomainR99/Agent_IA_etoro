# Agent IA eToro

Application qui propose un sujet de post pour investisseurs sur eToro à partir des actualités France récentes.

**Application en ligne :** [https://agentiaetoro-h743wzhtd5n8eajrncwq6f.streamlit.app/](https://agentiaetoro-h743wzhtd5n8eajrncwq6f.streamlit.app/)

## Fonctionnalités

- **Actualités France** : récupération des dernières actualités via News API
- **Post eToro** : génération d’un post pour investisseurs via OpenAI à partir des actualités

## Technologies

- **Frontend** : Streamlit
- **Backend** : Python (News API, OpenAI)
- **APIs** : News API (actualités France), OpenAI (génération du post)

## Installation

```bash
git clone <repo>
cd Agent_IA_etoro
python -m venv venv
source venv/bin/activate   # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
```

Créez un fichier `.env` à la racine :

```
OPENAI_API_KEY=votre_cle_openai
apiKey=votre_cle_news_api
```

## Lancement

```bash
streamlit run app.py
```

## Structure du projet

```
├── app.py                 # Application Streamlit
├── backend/
│   ├── news_fetcher.py    # Récupération des actualités (News API)
│   └── post_generator.py  # Génération du post (OpenAI)
├── prompts/
│   └── prompt_post_etoro.txt
└── requirements.txt
```
