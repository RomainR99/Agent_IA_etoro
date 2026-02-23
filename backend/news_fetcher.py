"""Récupération des actualités France via News API."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"


def fetch_france_news(api_key: str = None) -> dict:
    """
    Récupère les actualités France via News API.
    :param api_key: clé API News (ou depuis env si non fournie)
    :return: dict avec status, articles, totalResults
    """
    key = api_key or os.environ.get("apiKey")
    if not key:
        raise ValueError("Clé News API manquante. Ajoutez apiKey dans le fichier .env.")
    resp = requests.get(
        NEWS_API_URL,
        params={"country": "fr", "apiKey": key, "pageSize": 10},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()
