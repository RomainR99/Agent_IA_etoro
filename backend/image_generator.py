"""Génération d'une image OpenAI (DALL-E 3) à partir du post eToro."""
import base64
import os
from pathlib import Path

import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

PROMPT_IMAGE_PATH = Path(__file__).resolve().parent.parent / "prompts" / "prompt_image_etoro.txt"


def _load_image_prompt_system() -> str:
    """Charge le prompt système pour la génération du prompt image."""
    with open(PROMPT_IMAGE_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def _create_image_prompt(post_text: str, client: OpenAI) -> str:
    """Utilise GPT pour créer un prompt image professionnel à partir du post."""
    try:
        system_prompt = _load_image_prompt_system()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Post eToro à illustrer :\n\n{post_text[:1500]}"},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except openai.RateLimitError:
        raise ValueError("Quota API dépassé. Vérifiez votre facturation sur platform.openai.com.")
    except openai.APIConnectionError:
        raise ValueError("Impossible de se connecter à l'API OpenAI. Vérifiez votre connexion.")
    except openai.APIError as e:
        raise ValueError(f"Erreur API OpenAI : {e}") from e


def generate_post_image(post_text: str) -> bytes:
    """
    Génère une image DALL-E 3 illustrant le post.
    :param post_text: contenu du post eToro
    :return: bytes de l'image PNG
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY manquante dans .env ou Secrets.")
    client = OpenAI(api_key=api_key)
    prompt = _create_image_prompt(post_text, client)
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            response_format="b64_json",
            n=1,
        )
        b64 = response.data[0].b64_json
        return base64.b64decode(b64)
    except openai.RateLimitError:
        raise ValueError("Quota API dépassé. Vérifiez votre facturation sur platform.openai.com.")
    except openai.APIConnectionError:
        raise ValueError("Impossible de se connecter à l'API OpenAI. Vérifiez votre connexion.")
    except openai.APIError as e:
        raise ValueError(f"Erreur API OpenAI : {e}") from e
