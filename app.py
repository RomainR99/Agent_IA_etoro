"""
Application Streamlit : Agent IA eToro – Sujet de post pour investisseurs.
- Actualités France (News API)
- Génération d’un post eToro via OpenAI
"""
import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from backend.news_fetcher import fetch_france_news
from backend.post_generator import generate_post

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
st.caption("Actualités France et proposition de post pour investisseurs.")

# Charger les actualités
if "news" not in st.session_state:
    with st.spinner("Chargement des actualités France…"):
        try:
            data = fetch_france_news()
            st.session_state["news"] = data
        except Exception as e:
            st.error(f"Erreur News API : {e}")
            st.stop()

news = st.session_state.get("news", {})
articles = news.get("articles", [])

if not articles:
    st.warning("Aucune actualité disponible.")
    st.stop()

# Section 1 : Actualités France (News API – apiKey)
st.subheader("Actualités France (News API)")
news_text_parts = []
for i, art in enumerate(articles[:10], 1):
    title = art.get("title") or "Sans titre"
    desc = art.get("description") or ""
    source = art.get("source", {}).get("name", "")
    date = art.get("publishedAt", "")[:10] if art.get("publishedAt") else ""
    st.markdown(f"**{i}. {title}**")
    if desc:
        st.caption(desc)
    if source or date:
        st.caption(f"_{source} — {date}_" if source and date else f"_{source or date}_")
    st.divider()
    news_text_parts.append(f"- {title}" + (f" : {desc}" if desc else ""))

news_text = "\n".join(news_text_parts)

# Section 2 : Génération du post (OpenAI)
st.subheader("Post proposé pour investisseurs eToro")

generate_btn = st.button("Générer le post", type="primary")

if generate_btn:
    with st.spinner("Génération du post avec OpenAI…"):
        try:
            post = generate_post(news_text)
            st.session_state["post"] = post
            st.session_state["post_generated"] = True
        except Exception as e:
            st.error(f"Erreur OpenAI : {e}")

if st.session_state.get("post_generated") and st.session_state.get("post"):
    st.markdown("---")
    st.markdown(st.session_state["post"])
else:
    st.info("Cliquez sur « Générer le post » pour créer une proposition de post eToro à partir des actualités.")
