import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Configuration de la page
st.set_page_config(page_title="Assistant Réforme VPH", layout="wide")

# TITRE
st.title("🦽 Assistant Sélection Fauteuils Roulants (Réforme 2026)")

# --- LOGIQUE DE MISE À JOUR ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=60) # Mise à jour toutes les 60 secondes (1 minute)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df = df.replace(["Non spécifié", "null", "nan"], "")
        # On capture l'heure de la mise à jour (Heure de Paris)
        paris_tz = pytz.timezone('Europe/Paris')
        now = datetime.now(paris_tz).strftime("%d/%m/%Y à %H:%M")
        return df, now
    except Exception as e:
        return None, None

data, last_update = load_data()

# Affichage de la date de mise à jour en petit sous le titre
if last_update:
    st.caption(f"Status : Données synchronisées le {last_update}")

st.markdown("---")

if data is not None:
    # --- BARRE LATÉRALE (FILTRES) ---
    st.sidebar.header("🔍 Filtres de sélection")
    recherche = st.sidebar.text_input("Recherche rapide (Modèle, LPPR, Ref...)")
    
    # Filtre par Référence (CODE_REF)
    ref_list = []
    if "CODE_REF" in data.columns:
        ref_list = sorted([str(x) for x in data["CODE_REF"].unique() if x != ""])
    ref_choice = st.sidebar.multiselect("Référence Produit (CODE_REF)", ref_list)
    
    # Autres filtres
    cat_list = sorted(data["CATEGORIE"].unique()) if "CATEGORIE" in data.columns else []
    fab_list = sorted(data["FABRICANT"].unique()) if "FABRICANT" in data.columns else []
    
    cat_choice = st.sidebar.multiselect("Type de matériel", cat_list)
    fab_choice = st.sidebar.multiselect("Fabricant", fab_list)

    # --- LOGIQUE DE FILTRAGE ---
    df = data.copy()
    if recherche:
        df = df[df.apply(lambda row: recherche.lower() in row.astype(str).str.lower().values, axis=1)]
    if ref_choice:
        df = df[df["CODE_REF"].astype(str).isin(ref_choice)]
    if cat_choice:
        df = df[df["CATEGORIE"].isin(cat_choice)]
    if fab_choice:
        df = df[df["FABRICANT"].isin(fab_choice)]

    st.write(f"**{len(df)}** modèles trouvés.")

    # --- AFFICHAGE DES RÉSULTATS ---
    cols = st.columns(2)
    for idx, row in df.iterrows():
        with cols[idx % 2]:
            with st.container(border=True):
                st.subheader(f"{row.get('FABRICANT', '')} - {row.get('MODELE', '')}")
                c1, c2 = st.columns([1, 2])
                with c1:
                    img = row.get('LIEN PHOTO', '')
                    if str(img).startswith('http'):
                        st.image(img, use_container_width=True)
                    else:
                        st.info("📷 Image")
                with c2:
                    st.write(f"**Réf :** `{row.get('CODE_REF', 'N/A')}`")
                    st.write(f"**LPPR :** `{row.get('CODE_LPPR', '')}`")
                
                with st.expander("📝 Libellé de prescription"):
                    libelle = row.get('LIBELLE_PRESCRIPTION', '')
                    if libelle:
                        st.write(libelle)
                        if st.button("Copier", key=f"cp_{idx}"):
                            st.copy_to_clipboard(libelle)
                            st.toast("Copié !")
                    else:
                        st.write("À compléter dans le Sheet.")
else:
    st.error("⚠️ Erreur de lecture du Google Sheet.")
