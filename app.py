import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Configuration de la page
st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .filter-box { background-color: #e1f5fe; padding: 20px; border-radius: 15px; border-left: 8px solid #0288d1; margin-bottom: 20px; }
    .doc-card { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px 5px 0px 0px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #0288d1 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CHARGEMENT DES DONNÉES ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df = df.replace(["Non spécifié", "null", "nan"], "")
        paris_tz = pytz.timezone('Europe/Paris')
        now = datetime.now(paris_tz).strftime("%H:%M")
        return df, now
    except:
        return None, None

data, last_update = load_data()

# --- TITRE PRINCIPAL ---
st.title("🦽 Assistant Réforme VPH 2026")
if last_update:
    st.caption(f"✅ Dernière synchronisation des données : {last_update}")

# --- CRÉATION DES ONGLETS ---
tab1, tab2 = st.tabs(["🔎 CATALOGUE VPH", "📂 DOCUMENTS & DÉMARCHES"])

# ==========================================
# ONGLET 1 : CATALOGUE
# ==========================================
with tab1:
    if data is not None:
        # Zone de filtres
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            recherche = st.text_input("📝 Recherche libre :", placeholder="Modèle, marque, code...")
            cat_list = sorted(data["CATEGORIE"].unique()) if "CATEGORIE" in data.columns else []
            cat_choice = st.multiselect("⚙️ Type de matériel :", cat_list)
        with col2:
            ref_list = sorted([str(x) for x in data["CODE_REF"].unique() if x != ""]) if "CODE_REF" in data.columns else []
            ref_choice = st.multiselect("🔢 Référence (CODE_REF) :", ref_list)
            fab_list = sorted(data["FABRICANT"].unique()) if "FABRICANT" in data.columns else []
            fab_choice = st.multiselect("🏭 Fabricant :", fab_list)
        st.markdown('</div>', unsafe_allow_html=True)

        # Filtrage
        df = data.copy()
        if recherche:
            df = df[df.apply(lambda row: recherche.lower() in row.astype(str).str.lower().values, axis=1)]
        if ref_choice:
            df = df[df["CODE_REF"].astype(str).isin(ref_choice)]
        if cat_choice:
            df = df[df["CATEGORIE"].isin(cat_choice)]
        if fab_choice:
            df = df[df["FABRICANT"].isin(fab_choice)]

        st.write(f"💡 **{len(df)}** modèles trouvés.")
        
        # Affichage
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
        st.error("Erreur de chargement du catalogue.")

# ==========================================
# ONGLET 2 : DOCUMENTS PDF & DÉMARCHES
# ==========================================
with tab2:
    st.header("📚 Bibliothèque de documents")
    st.info("Retrouvez ici tous les documents nécessaires à l'évaluation et à la prescription.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("📋 Fiches de préconisation")
        with st.container(border=True):
            st.write("**Fiche d'évaluation des besoins**")
            st.link_button("📥 Télécharger PDF", "https://VOTRE_LIEN_ICI_1.pdf")
        
        with st.container(border=True):
            st.write("**Fiche de préconisation technique**")
            st.link_button("📥 Télécharger PDF", "https://VOTRE_LIEN_ICI_2.pdf")

    with col_b:
        st.subheader("📑 Démarches & Guides")
        with st.container(border=True):
            st.write("**Guide des démarches administratives**")
            st.link_button("📥 Voir le guide", "https://VOTRE_LIEN_ICI_3.pdf")
            
        with st.container(border=True):
            st.write("**Tableau récapitulatif des classes**")
            st.link_button("📥 Ouvrir le document", "https://VOTRE_LIEN_ICI_4.pdf")

    st.markdown("---")
    st.warning("⚠️ **Rappel :** Assurez-vous d'utiliser les versions à jour (Réforme Mars 2026).")
