"""Génération de la lettre de motivation via Groq."""
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "prompt_lettre_motivation.txt"


def load_system_prompt() -> str:
    """Charge le prompt système depuis le fichier."""
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def generate_letter(cv_text: str, context: str, language: str = "fr") -> str:
    """
    Génère une lettre de motivation à partir du CV et du contexte (offre, poste, etc.).
    :param cv_text: texte extrait du CV
    :param context: description du poste / offre / instructions
    :param language: langue de la lettre (fr par défaut)
    :return: texte de la lettre de motivation
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Variable d'environnement GROQ_API_KEY manquante. Ajoutez-la dans un fichier .env.")
    client = Groq(api_key=api_key)
    system_prompt = load_system_prompt()
    user_content = f"""Voici le CV du candidat (texte extrait) :

---
{cv_text}
---

Contexte / offre / instructions pour la lettre :
---
{context}
---

Rédige la lettre de motivation en {language}."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()
