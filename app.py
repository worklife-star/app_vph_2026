import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# --- CHARGEMENT DES DONNÉES ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return None

df_raw = load_data()

# --- INTERFACE ---
st.title("🦽 Assistant Réforme VPH 2026")

if df_raw is not None:
    df = df_raw.copy()

    # --- RECHERCHE TEXTUELLE ---
    recherche = st.text_input("🔍 Rechercher un modèle (ex: Action, TDX, Kuschall...)", "").strip()

    # --- FILTRES EN HAUT DE PAGE ---
    st.markdown("### 🎛️ Filtres")
    f1, f2, f3, f4, f5 = st.columns(5)

    def get_options(col):
        """Retourne les valeurs uniques triées d'une colonne, avec 'Tous' en premier."""
        if col in df.columns:
            vals = sorted(df[col].dropna().astype(str).unique().tolist())
            return ["Tous"] + vals
        return ["Tous"]

    with f1:
        filtre_categorie = st.selectbox("📁 Catégorie", get_options("CATEGORIE"))
    with f2:
        filtre_fabricant = st.selectbox("🏭 Fabricant", get_options("FABRICANT"))
    with f3:
        filtre_chassis = st.selectbox("🔩 Châssis", get_options("CHASSIS"))
    with f4:
        filtre_ref = st.selectbox("🔖 Code Réf.", get_options("CODE_REF"))
    with f5:
        filtre_sous_type = st.selectbox("📂 Sous-type", get_options("SOUS_TY
