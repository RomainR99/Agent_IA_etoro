"""Génération du post eToro via OpenAI."""
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "prompt_post_etoro.txt"


def load_system_prompt() -> str:
    """Charge le prompt système depuis le fichier."""
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def generate_post(news_text: str) -> str:
    """
    Génère un sujet de post pour investisseurs eToro à partir des actualités.
    :param news_text: résumé des actualités récentes
    :return: texte du post proposé
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Variable d'environnement OPENAI_API_KEY manquante. Ajoutez-la dans .env.")
    client = OpenAI(api_key=api_key)
    system_prompt = load_system_prompt()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Texte fourni :\n\n{news_text}\n\nGénère le post eToro."},
        ],
        temperature=0.6,
    )
    return response.choices[0].message.content.strip()
