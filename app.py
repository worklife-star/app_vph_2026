import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# --- CHARGEMENT DES DONNÉES ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=5) # Mise à jour toutes les 5 secondes pour tes tests
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        
        # --- NETTOYAGE CRITIQUE DES COLONNES ---
        # On enlève les espaces et les "_" et on met en MAJUSCULES
        # Ainsi "fiche_technique" ou "FICHE TECHNIQUE" deviennent "FICHETECHNIQUE"
        raw_cols = df.columns.tolist()
        df.columns = [str(c).strip().upper().replace(' ', '').replace('_', '') for c in df.columns]
        
        # Suppression des lignes vides
        df = df.dropna(how='all')
        df = df.fillna("")
        
        return df, raw_cols
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return None, []

data, original_cols = load_data()

# --- INTERFACE ---
st.title("🦽 Assistant Réforme VPH 2026")

if data is not None:
    # Barre de recherche
    recherche = st.text_input("🔍 Rechercher un modèle, une marque, etc.")
    
    df_f = data.copy()
    if recherche:
        mask = df_f.astype(str).apply(lambda x: x.str.contains(recherche, case=False)).any(axis=1)
        df_f = df_f[mask]

    # Affichage en grille (2 colonnes)
    cols = st.columns(2)
    
    for idx, (_, row) in enumerate(df_f.iterrows()):
        with cols[idx % 2]:
            # Carte du produit
            with st.container(border=True):
                st.subheader(f"{row.get('FABRICANT', '')} - {row.get('MODELE', '')}")
                
                col_gauche, col_droite = st.columns([1, 1.5])
                
                with col_gauche:
                    # 1. LA PHOTO
                    img_url = str(row.get('LIENPHOTO', '')).strip()
                    if img_url.lower().startswith('http'):
                        st.image(img_url, use_container_width=True)
                    else:
                        st.info("📷 Image non dispo")
                    
                    # 2. LA FICHE TECHNIQUE (JUSTE EN DESSOUS DE LA PHOTO)
                    # On cherche la colonne nettoyée "FICHETECHNIQUE"
                    fiche_url = str(row.get('FICHETECHNIQUE', '')).strip()
                    
                    if fiche_url.lower().startswith('http'):
                        st.link_button("📄 VOIR FICHE TECHNIQUE", fiche_url, use_container_width=True, type="primary")
                    else:
                        # Petit message si le lien est manquant dans ton Sheet
                        st.caption("⚠️ Fiche technique non renseignée")

                with col_droite:
                    st.write(f"**Réf :** `{row.get('CODEREF', 'N/A')}`")
                    st.write(f"**LPPR :** `{row.get('CODELPPR', 'N/A')}`")
                    st.write(f"**Châssis :** {row.get('CHASSIS', '-')}")
                    st.write(f"**Dossier :** {row.get('DOSSIER', '-')}")
                    st.write(f"**Catégorie :** {row.get('CATEGORIE', '-')}")
                
                # Libellé en bas de carte
                libelle = row.get('LIBELLEPRESCRIPTION', '')
                if libelle and libelle != "Non spécifié":
                    with st.expander("📝 Libellé de prescription"):
                        st.write(libelle)
                        if st.button("Copier", key=f"cp_{idx}"):
                            st.copy_to_clipboard(libelle)
                            st.toast("Copié !")
