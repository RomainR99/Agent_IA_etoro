"""Génération de recommandations d'amélioration du CV via Groq."""
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "prompt_recommandations_cv.txt"


def _load_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def get_cv_recommendations(cv_text: str, language: str = "fr") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    system_prompt = _load_prompt()
    lang_label = "français" if language == "fr" else "English"
    user_content = f"""Voici le CV à analyser (texte extrait) :

---
{cv_text}
---

Rédige tes recommandations d'amélioration en {lang_label}."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
