# Coach IA – CV et lettres de motivation

Application web qui vous aide à préparer vos candidatures : génération de lettres de motivation personnalisées à partir de votre CV et recommandations pour améliorer votre CV.

**Application en ligne :** [https://coachiacvlettres-supkddtyk6rjif6ehmwnkz.streamlit.app/](https://coachiacvlettres-supkddtyk6rjif6ehmwnkz.streamlit.app/)

## Fonctionnalités

- **Import du CV** : glisser-déposer un CV au format PDF ou DOCX
- **Lettre de motivation** : saisissez le contexte (poste, entreprise, offre) et générez une lettre adaptée à votre profil et à l’offre
- **Recommandations d’amélioration du CV** : analyse de votre CV et conseils concrets (structure, formulation, mise en valeur des compétences)
- **Export** : téléchargement de la lettre en PDF et en DOCX

## Technologies

- **Frontend** : Streamlit
- **Backend** : Python (extraction de texte PDF/DOCX, génération via API Groq)
- **Modèle** : Llama (Groq)

## Installation

```bash
git clone <repo>
cd Coach_IA_pour_CV_et_lettres_de_motivation
python -m venv venv
source venv/bin/activate   # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
```

Créez un fichier `.env` à la racine avec votre clé API Groq :

```
GROQ_API_KEY=votre_cle_api
```

## Lancement

```bash
streamlit run app.py
```

L’application s’ouvre dans le navigateur (par défaut sur `http://localhost:8501`).

## Structure du projet

```
├── app.py                 # Application Streamlit
├── backend/
│   ├── cv_parser.py       # Extraction du texte du CV (PDF/DOCX)
│   ├── letter_generator.py # Génération de la lettre de motivation
│   ├── cv_recommendations.py # Recommandations d'amélioration du CV
│   └── export.py          # Export PDF et DOCX
├── prompts/
│   ├── prompt_lettre_motivation.txt
│   └── prompt_recommandations_cv.txt
└── requirements.txt
```
