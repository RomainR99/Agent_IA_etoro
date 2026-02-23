"""
Application Streamlit : Agent IA eToro – Sujet de post pour investisseurs.
- Saisie ou copier-coller d'un texte (actualités, infos…)
- Génération d'un post eToro via OpenAI
"""
import os
import streamlit as st
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
try:
    if hasattr(st, "secrets") and st.secrets:
        if "OPENAI_API_KEY" in st.secrets and not os.environ.get("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = str(st.secrets["OPENAI_API_KEY"])
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from backend.post_generator import generate_post
from backend.image_generator import create_image_prompt_options, generate_post_image

st.set_page_config(
    page_title="Agent IA eToro",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    h1 { color: #1e3a5f; }
</style>
""", unsafe_allow_html=True)

st.title("📈 Agent IA eToro")
st.caption("Collez un texte (actualités, infos marché…) et générez un post pour investisseurs eToro.")

# Encadré de saisie
st.subheader("Texte source")
input_text = st.text_area(
    "Collez ou saisissez ici le texte à transformer en post eToro (actualités, analyses, communiqués…)",
    placeholder="Exemple : Selon les derniers chiffres, l'inflation en zone euro a ralenti à 2,4% en janvier…",
    height=200,
    label_visibility="collapsed",
)

# Génération du post
st.subheader("Post proposé pour investisseurs eToro")

generate_btn = st.button("Générer le post", type="primary")

if generate_btn:
    if not input_text or not input_text.strip():
        st.error("Veuillez saisir ou coller un texte avant de générer le post.")
    else:
        with st.spinner("Génération du post avec OpenAI…"):
            try:
                post = generate_post(input_text.strip())
                st.session_state["post"] = post
                st.session_state["post_generated"] = True
                st.session_state.pop("post_image", None)
                st.session_state.pop("post_image_error", None)
                st.session_state.pop("prompt_options", None)
            except Exception as e:
                st.error(f"Erreur : {e}")
                st.stop()
        with st.spinner("Proposition des 3 prompts image…"):
            try:
                st.session_state["prompt_options"] = create_image_prompt_options(post)
                st.session_state.pop("post_image_error", None)
            except Exception as e:
                st.session_state["post_image_error"] = str(e)

if st.session_state.get("post_generated") and st.session_state.get("post"):
    st.markdown("---")
    st.markdown(st.session_state["post"])

    prompt_options = st.session_state.get("prompt_options")
    if prompt_options:
        st.subheader("Choisir le prompt pour l'image")
        selected = st.radio(
            "Sélectionnez un prompt :",
            range(len(prompt_options)),
            format_func=lambda i: f"Prompt {i+1}",
            label_visibility="collapsed",
        )
        with st.expander("Voir les prompts", expanded=True):
            for i, p in enumerate(prompt_options):
                st.caption(f"**Prompt {i+1}**")
                st.text(p)
        if st.button("Générer l'image", type="primary"):
            with st.spinner("Génération de l'image…"):
                try:
                    img_bytes = generate_post_image(prompt_options[selected])
                    st.session_state["post_image"] = img_bytes
                    st.session_state.pop("post_image_error", None)
                    st.rerun()
                except Exception as e:
                    st.session_state["post_image_error"] = str(e)
                    st.error(f"Erreur : {e}")

    if st.session_state.get("post_image"):
        st.subheader("Image proposée")
        st.image(st.session_state["post_image"], use_container_width=True)
        st.download_button(
            "Télécharger l'image",
            data=st.session_state["post_image"],
            file_name="post_etoro.png",
            mime="image/png",
            type="primary",
        )
    elif st.session_state.get("post_image_error") and not prompt_options:
        st.warning(
            "Image non générée (quota API ou facturation OpenAI). "
            "Vérifiez votre compte sur platform.openai.com."
        )
else:
    st.info("Collez un texte dans la zone ci-dessus, puis cliquez sur « Générer le post ».")
