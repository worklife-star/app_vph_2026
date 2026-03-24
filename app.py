import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# --- STYLE CSS POUR L'INTERFACE ---
st.markdown("""
    <style>
    .stContainer {
        background-color: #ffffff;
    }
    .pdf-link {
        display: inline-block;
        padding: 8px 12px;
        background-color: #0288d1;
        color: white !important;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 10px;
    }
    .pdf-link:hover {
        background-color: #01579b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CHARGEMENT DES DONNÉES ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        # Lecture du CSV via Google Sheets
        df = pd.read_csv(SHEET_URL)
        # Nettoyage des noms de colonnes : suppression des espaces et mise en majuscules
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erreur lors de la lecture du Google Sheet : {e}")
        return None

df_raw = load_data()

# --- ENTÊTE ---
st.title("🦽 Assistant Réforme VPH 2026")
st.markdown("---")

# --- BARRE DE RECHERCHE ---
recherche = st.text_input("🔍 Rechercher par modèle, fabricant ou code (ex: TDX, Action, 9561616...)", "").strip()

if df_raw is not None:
    # Filtrage des données
    df = df_raw.copy()
    if recherche:
        # Recherche dans toutes les colonnes sans tenir compte de la casse
        mask = df.astype(str).apply(lambda x: x.str.contains(recherche, case=False)).any(axis=1)
        df = df[mask]

    st.write(f"💡 **{len(df)}** modèles correspondent à votre recherche.")

    # --- AFFICHAGE DES RÉSULTATS (GRILLE) ---
    cols = st.columns(2)
    
    for idx, (i, row) in enumerate(df.iterrows()):
        with cols[idx % 2]:
            with st.container(border=True):
                # TITRE DU PRODUIT
                st.subheader(f"{row.get('FABRICANT', '')} - {row.get('MODELE', '')}")
                
                c1, c2 = st.columns([1, 1.3])
                
                with c1:
                    # GESTION DE LA PHOTO
                    photo = str(row.get('LIEN PHOTO', '')).strip()
                    if photo.lower().startswith("http"):
                        st.image(photo, use_container_width=True)
