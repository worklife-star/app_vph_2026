import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import logging
import re

# ─────────────────────────────────────────────

# CONFIGURATION

# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Expert VPH 2026",
    layout="wide",
    page_icon="🦽",
)

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"
)

# Colonnes attendues après normalisation (UPPER + strip)
COL_FABRICANT = "FABRICANT"
COL_MODELE = "MODELE"
COL_CATEGORIE = "CATEGORIE"
COL_PHOTO = "LIEN PHOTO"
COL_PDF = "FICHE TECHNIQUE"
COL_REF = "CODE_REF"
COL_LPPR = "CODE_LPPR"
COL_CHASSIS = "CHASSIS"
COL_LIBELLE = "LIBELLE_PRESCRIPTION"

# ─────────────────────────────────────────────

# CONFIGURATION DU LOGGER

# ─────────────────────────────────────────────

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────

# CHARGEMENT DES DONNÉES

# ─────────────────────────────────────────────

@st.cache_data(ttl=300)  # 5 min — évite les rechargements trop fréquents
def load_data() -> pd.DataFrame:
    try:
        df = pd.read_csv(SHEET_URL, dtype=str)  # tout en str dès le départ
        df.columns = [str(c).strip().upper() for c in df.columns]
        df = df.fillna("")  # évite les NaN dans les .get()
        return df
    except Exception as e:
        logger.error(f"Erreur de lecture du fichier : {e}")
        st.error(f"❌ Erreur de lecture du fichier : {e}")
        return None

def safe_get(row: pd.Series, col: str, default: str = "-") -> str:
    """Lecture sécurisée d’une cellule avec valeur par défaut."""
    val = row.get(col, default)
    return
