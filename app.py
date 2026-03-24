import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .filter-box { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #dee2e6; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px 5px 0px 0px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #0288d1 !important; color: white !important; }
    
    /* Style des cartes */
    .vph-card {
        padding: 15px;
        border-radius: 12px;
        border-left: 10px solid #ccc; /* Couleur par défaut */
        margin-bottom: 15px;
        background-color: white;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTION DE COULEUR PAR CATÉGORIE ---
def get_cat_color(categorie):
    cat = str(categorie).upper()
    if "MANUEL" in cat: return "#0288d1" # Bleu
    if "ÉLECTRIQUE" in cat or "ELECTRIQUE" in cat: return "#f57c00" # Orange
    if "SPORT" in cat: return "#388e3c" # Vert
    if "ENFANT" in cat: return "#d32f2f" # Rouge
    if "POSITIONNEMENT" in cat: return "#7b1fa2" # Violet
    return "#9e9e9e" # Gris par défaut

# --- CHARGEMENT DES DONNÉES ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df = df.dropna(how='all')
        if "MODELE" in df.columns:
            df = df[df["MODELE"].notna() & (df["MODELE"] != "")]
        df = df.replace(["Non spécifié", "null", "nan", "NaN"], "")
        paris_tz = pytz.timezone('Europe/Paris')
        now = datetime.now(paris_tz).strftime("%H:%M")
        return df, now
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        return None, None

data, last_update = load_data()

# --- TITRE PRINCIPAL ---
st.title("🦽 Assistant Réforme VPH 2026")
if last_update:
    st.caption(f"✅ Données synchronisées à {last_update}")

tab1, tab2 = st.tabs(["🔎 CATALOGUE VPH", "📂 DOCUMENTS & DÉMARCHES"])

# ==========================================
# ONGLET 1 : CATALOGUE
# ==========================================
with tab1:
    if data is not None and not data.empty:
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            recherche = st.text_input("📝 Recherche libre :", placeholder="Modèle, Marque, Châssis...")
            cat_list = sorted([x for x in data["CATEGORIE"].unique() if str(x) != ""]) if "CATEGORIE" in data.columns else []
            cat_choice = st.multiselect("⚙️ Type de matériel :", cat_list)
        with col2:
            fab_list = sorted([x for x in data["FABRICANT"].unique() if str(x) != ""]) if "FABRICANT" in data.columns else []
            fab_choice = st.multiselect("🏭 Fabricant :", fab_list)
            ref_list = sorted([str(x) for x in data["CODE_REF"].unique() if str(x) != ""]) if "CODE_REF" in data.columns else []
            ref_choice = st.multiselect("🔢 Référence (CODE_REF) :", ref_list)
        st.markdown('</div>', unsafe_allow_html=True)

        # Filtrage
        df_f = data.copy()
        if recherche:
            mask = df_f.astype(str).apply(lambda x: x.str.contains(recherche, case=False)).any(axis=1)
            df_f = df_f[mask]
        if cat_choice: df_f = df_f[df_f["CATEGORIE"].isin(cat_choice)]
        if fab_choice: df_f = df_f[df_f["FABRICANT"].isin(fab_choice)]
        if ref_choice: df_f = df_f[df_f["CODE_REF"].astype(str).isin(ref_choice)]

        st.write(f"💡 **{len(df_f)}** modèles trouvés.")
        
        # Affichage
        cols = st.columns(2)
        for idx, (_, row) in enumerate(df_f.iterrows()):
            cat_color = get_cat_color(row.get('CATEGORIE', ''))
            with cols[idx % 2]:
                # On utilise du HTML pour la bordure colorée personnalisée
                st.markdown(f"""
                    <div style="border-left: 8px solid {cat_color}; padding: 15px; border-radius: 10px; background-color: #ffffff; border-right: 1px solid #eee; border-top: 1px solid #eee; border-bottom: 1px solid #eee; margin-bottom: 20px;">
                        <h3 style="margin-top:0;">{row.get('FABRICANT', '')} - {row.get('MODELE', '')}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.container():
                    c1, c2 = st.columns([1, 1.5])
                    with c1:
                        img = row.get('LIEN PHOTO', '')
                        if str(img).startswith('http'):
                            st.image(img, use_container_width=True)
                        else:
                            st.info("📷 Image non dispo")
                        
                        ft = row.get('FICHE TECHNIQUE', '')
                        if str(ft).startswith('http'):
                            st.link_button("📄 Fiche Technique", ft, use_container_width=True)

                    with c2:
                        st.markdown(f"**Réf :** `{row.get('CODE_REF', 'N/A')}`")
                        st.markdown(f"**LPPR :** `{row.get('CODE_LPPR', 'N/A')}`")
                        st.markdown(f"**Catégorie :** <span style='color:{cat_color}; font-weight:bold;'>{row.get('CATEGORIE', 'N/A')}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Châssis :** {row.get('CHASSIS', '-')}")
                        st.markdown(f"**Dossier :** {row.get('DOSSIER', '-')}")
                    
                    libelle = row.get('LIBELLE_PRESCRIPTION', '')
                    if libelle:
                        with st.expander("📝 Libellé de prescription"):
                            st.write(libelle)
                            if st.button("Copier", key=f"cp_{idx}"):
                                st.copy_to_clipboard(libelle)
                                st.toast("Copié !")
                st.markdown("---")

# ==========================================
# ONGLET 2 : DOCUMENTS
# ==========================================
with tab2:
    st.header("📚 Bibliothèque de documents")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📋 Fiches de préconisation")
        st.link_button("📥 Fiche d'évaluation", "https://drive.google.com/file/d/1aEwrr1jAEMQE1pEiOUVs3ShwIXTKYDJ8/view")
    with col_b:
        st.subheader("📑 Démarches & Guides")
        st.link_button("📥 Guide des démarches", "https://drive.google.com/file/d/1TXF4AiB_U9cwE1_56HoVrsCIE-RGZKLo/view")
