"""Génération d'une image OpenAI (DALL-E 3) à partir du post eToro."""
import base64
import os
from pathlib import Path

import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

PROMPT_IMAGE_PATH = Path(__file__).resolve().parent.parent / "prompts" / "prompt_image_etoro.txt"

# Préfixe ajouté en dur au début de chaque prompt image
PROMPT_IMAGE_PREFIX = (
    "Cartoon style illustration, vivid colors, bold outlines, dynamic composition, no text, no speech bubbles."
)


def _load_image_prompt_system() -> str:
    """Charge le prompt système pour la génération du prompt image."""
    with open(PROMPT_IMAGE_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def _create_image_prompts(post_text: str, client: OpenAI) -> list[str]:
    """Utilise GPT pour créer 3 prompts image différents à partir du post."""
    try:
        system_prompt = (
            _load_image_prompt_system()
            + "\n\nPropose exactement 3 variantes de prompts, numérotées 1, 2, 3, une par ligne. "
            "Format : 1. [prompt] 2. [prompt] 3. [prompt]"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Post eToro à illustrer :\n\n{post_text[:1500]}"},
            ],
            temperature=0.8,
        )
        text = response.choices[0].message.content.strip()
        prompts = []
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            for prefix in ("1.", "2.", "3.", "1)", "2)", "3)"):
                if line.lower().startswith(prefix):
                    prompt = line[len(prefix) :].strip().lstrip(".- )")
                    if len(prompt) > 5:
                        prompts.append(f"{PROMPT_IMAGE_PREFIX} {prompt}")
                    break
        while len(prompts) < 3:
            prompts.append(PROMPT_IMAGE_PREFIX)
        return prompts[:3]
    except openai.RateLimitError:
        raise ValueError("Quota API dépassé. Vérifiez votre facturation sur platform.openai.com.")
    except openai.APIConnectionError:
        raise ValueError("Impossible de se connecter à l'API OpenAI. Vérifiez votre connexion.")
    except openai.APIError as e:
        raise ValueError(f"Erreur API OpenAI : {e}") from e


def create_image_prompt_options(post_text: str) -> list[str]:
    """Retourne 3 propositions de prompts pour l'image."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY manquante dans .env ou Secrets.")
    client = OpenAI(api_key=api_key)
    return _create_image_prompts(post_text, client)


def generate_post_image(prompt: str) -> bytes:
    """
    Génère une image DALL-E 3 à partir du prompt fourni.
    :param prompt: prompt complet pour DALL-E 3
    :return: bytes de l'image PNG
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY manquante dans .env ou Secrets.")
    client = OpenAI(api_key=api_key)
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
