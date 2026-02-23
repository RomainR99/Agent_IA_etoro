"""
Application Streamlit : Coach IA pour CV et lettres de motivation.
- Glisser-déposer un CV (PDF ou DOCX)
- Saisir le contexte (offre, poste, entreprise…)
- Générer une lettre de motivation
- Exporter en PDF et .docx
"""
import streamlit as st
import sys
from pathlib import Path

# Racine du projet
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from backend.cv_parser import extract_text_from_cv
from backend.letter_generator import generate_letter
from backend.cv_recommendations import get_cv_recommendations
from backend.export import export_to_pdf, export_to_docx

st.set_page_config(
    page_title="Coach IA – Lettre de motivation",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Style pour la zone de dépôt
st.markdown("""
<style>
    .uploadedFile { margin: 0.5rem 0; }
    [data-testid="stFileUploader"] {
        border: 2px dashed #4a90d9;
        border-radius: 8px;
        padding: 1.5rem;
        background: #f8fafc;
    }
    [data-testid="stFileUploader"] section { padding: 0.5rem; }
    h1 { color: #1e3a5f; }
</style>
""", unsafe_allow_html=True)

st.title("📄 Coach IA – Lettre de motivation")
st.caption("Uploadez votre CV, décrivez le poste ou l’offre, puis générez une lettre personnalisée.")

# Upload CV (drag & drop via file_uploader)
uploaded_file = st.file_uploader(
    "Glissez-déposez votre CV (PDF ou DOCX)",
    type=["pdf", "docx"],
    help="Formats acceptés : PDF, DOCX",
)

# Contexte : texte libre (offre, poste, entreprise…)
context = st.text_area(
    "Contexte pour la lettre",
    placeholder="Ex. : Poste de Développeur Python à Paris, entreprise X. Mission : développement backend, travail en agile…",
    height=120,
    help="Décrivez le poste, l’entreprise, l’offre ou toute consigne pour personnaliser la lettre.",
)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    generate_btn = st.button("Générer la lettre", type="primary", use_container_width=True)
with col2:
    lang = st.selectbox("Langue", ["fr", "en"], format_func=lambda x: "Français" if x == "fr" else "English")

# Génération
if generate_btn:
    if not uploaded_file:
        st.error("Veuillez déposer un CV (PDF ou DOCX).")
        st.stop()
    if not (context and context.strip()):
        st.error("Veuillez saisir le contexte (offre, poste, etc.).")
        st.stop()

    with st.spinner("Extraction du CV, génération de la lettre et des recommandations…"):
        try:
            # Sauvegarde temporaire pour le parser (il attend un chemin fichier)
            import tempfile
            suffix = Path(uploaded_file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            try:
                cv_text = extract_text_from_cv(tmp_path)
            finally:
                Path(tmp_path).unlink(missing_ok=True)

            if not cv_text or len(cv_text.strip()) < 50:
                st.warning("Peu de texte extrait du CV. Vérifiez que le fichier n’est pas une image scannée.")
            letter = generate_letter(cv_text, context.strip(), language=lang)
            recommendations = get_cv_recommendations(cv_text, language=lang)
            st.session_state["letter"] = letter
            st.session_state["recommendations"] = recommendations
            st.session_state["letter_generated"] = True
        except ValueError as e:
            st.error(str(e))
            st.stop()
        except Exception as e:
            st.error(f"Erreur : {e}")
            st.stop()

# Affichage de la lettre (éditable) + recommandations + export
if st.session_state.get("letter_generated") and st.session_state.get("letter"):
    st.subheader("Lettre de motivation générée")
    st.caption("Modifiez le texte ci-dessous, puis cliquez sur « Enregistrer » avant d'exporter.")
    # Formulaire : la valeur n'est lue qu'à l'envoi, ce qui garantit que l'export utilise la bonne version
    with st.form("letter_form"):
        edited_letter = st.text_area(
            "Contenu de la lettre",
            value=st.session_state["letter"],
            height=320,
            label_visibility="collapsed",
        )
        col_save, _ = st.columns([1, 3])
        with col_save:
            saved = st.form_submit_button("Enregistrer les modifications")
    if saved:
        st.session_state["letter"] = edited_letter
        st.success("Modifications enregistrées. Vous pouvez maintenant exporter en PDF ou DOCX.")
    letter_to_export = st.session_state["letter"]

    if st.session_state.get("recommendations"):
        with st.expander("Recommandations d'amélioration du CV", expanded=True):
            st.markdown(st.session_state["recommendations"])

    st.subheader("Exporter")
    pdf_bytes = export_to_pdf(letter_to_export)
    docx_bytes = export_to_docx(letter_to_export)
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "Télécharger en PDF",
            data=pdf_bytes,
            file_name="lettre_motivation.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "Télécharger en DOCX",
            data=docx_bytes,
            file_name="lettre_motivation.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

if not st.session_state.get("letter_generated"):
    st.info("Uploadez un CV et remplissez le contexte, puis cliquez sur « Générer la lettre ».")
