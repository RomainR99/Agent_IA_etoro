"""Génération d'une image OpenAI (DALL-E 3) à partir du post eToro."""
import base64
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def _create_image_prompt(post_text: str, client: OpenAI) -> str:
    """Utilise GPT pour créer un prompt image professionnel à partir du post."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Tu crées des prompts pour DALL-E 3. Réponds UNIQUEMENT par le prompt en anglais, "
                "2-3 phrases max. Style : infographie professionnelle, finance/investissement, "
                "design épuré, graphiques, tendances. Pas de texte dans l'image. Pas de visages.",
            },
            {"role": "user", "content": f"Post eToro à illustrer :\n\n{post_text[:1500]}"},
        ],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()


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
