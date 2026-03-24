import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .filter-box { background-color: #e1f5fe; padding: 20px; border-radius: 15px; border-left: 8px solid #0288d1; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px 5px 0px 0px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #0288d1 !important; color: white !important; }
    div[data-testid="stExpander"] { border: 1px solid #e0e0e0; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CHARGEMENT DES DONNÉES ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        # Lecture du CSV
        df = pd.read_csv(SHEET_URL)
        
        # 1. NETTOYAGE : Supprime les lignes totalement vides (souvent dues à l'agrandissement du tableau)
        df = df.dropna(how='all')
        
        # 2. NETTOYAGE : On garde seulement les lignes qui ont au moins un Modèle ou un Fabricant
        if "MODELE" in df.columns:
            df = df[df["MODELE"].notna() & (df["MODELE"] != "")]
        
        # Remplacement des valeurs bizarres par du vide
        df = df.replace(["Non spécifié", "null", "nan", "NaN"], "")
        
        # Gestion de l'heure de mise à jour
        paris_tz = pytz.timezone('Europe/Paris')
        now = datetime.now(paris_tz).strftime("%H:%M")
        return df, now
    except Exception as e:
        st.error(f"Erreur de connexion au Google Sheet : {e}")
        return None, None

data, last_update = load_data()

# --- TITRE PRINCIPAL ---
st.title("🦽 Assistant Réforme VPH 2026")
if last_update:
    st.caption(f"✅ Données synchronisées en direct de Google Sheets à {last_update}")

# --- CRÉATION DES ONGLETS ---
tab1, tab2 = st.tabs(["🔎 CATALOGUE VPH", "📂 DOCUMENTS & DÉMARCHES"])

# ==========================================
# ONGLET 1 : CATALOGUE
# ==========================================
with tab1:
    if data is not None and not data.empty:
        # Zone de filtres
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            recherche = st.text_input("📝 Recherche libre (Modèle, Marque, Code...) :", placeholder="Tapez votre recherche...")
            
            # Récupération dynamique des catégories (ne prend que celles qui ne sont pas vides)
            cat_list = sorted([x for x in data["CATEGORIE"].unique() if x != ""]) if "CATEGORIE" in data.columns else []
            cat_choice = st.multiselect("⚙️ Type de matériel :", cat_list)
            
        with col2:
            fab_list = sorted([x for x in data["FABRICANT"].unique() if x != ""]) if "FABRICANT" in data.columns else []
            fab_choice = st.multiselect("🏭 Fabricant :", fab_list)
            
            ref_list = sorted([str(x) for x in data["CODE_REF"].unique() if x != ""]) if "CODE_REF" in data.columns else []
            ref_choice = st.multiselect("🔢 Référence (CODE_REF) :", ref_list)
        st.markdown('</div>', unsafe_allow_html=True)

        # Filtrage logique
        df_filtered = data.copy()
        if recherche:
            # Recherche dans toutes les colonnes en même temps
            mask = df_filtered.astype(str).apply(lambda x: x.str.contains(recherche, case=False)).any(axis=1)
            df_filtered = df_filtered[mask]
        if cat_choice:
            df_filtered = df_filtered[df_filtered["CATEGORIE"].isin(cat_choice)]
        if fab_choice:
            df_filtered = df_filtered[df_filtered["FABRICANT"].isin(fab_choice)]
        if ref_choice:
            df_filtered = df_filtered[df_filtered["CODE_REF"].astype(str).isin(ref_choice)]

        st.write(f"💡 **{len(df_filtered)}** modèles correspondent à vos critères.")
        
        # Affichage en grille (2 colonnes)
        cols = st.columns(2)
        for idx, (_, row) in enumerate(df_filtered.iterrows()):
            with cols[idx % 2]:
                with st.container(border=True):
                    # En-tête de la carte
                    st.subheader(f"{row.get('FABRICANT', 'N/A')} - {row.get('MODELE', 'N/A')}")
                    
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        img_url = row.get('LIEN PHOTO', '')
                        if isinstance(img_url, str) and img_url.startswith('http'):
                            st.image(img_url, use_container_width=True)
                        else:
                            st.info("📷 Pas d'image disponible")
                            
                    with c2:
                        st.markdown(f"**Réf :** `{row.get('CODE_REF', 'N/A')}`")
                        st.markdown(f"**LPPR :** `{row.get('CODE_LPPR', 'N/A')}`")
                        st.markdown(f"**Catégorie :** {row.get('CATEGORIE', 'N/A')}")
                    
                    # Libellé avec bouton de copie
                    libelle = row.get('LIBELLE_PRESCRIPTION', '')
                    if libelle:
                        with st.expander("📝 Voir le libellé de prescription"):
                            st.write(libelle)
                            if st.button("Copier le libellé", key=f"btn_{idx}"):
                                st.copy_to_clipboard(libelle)
                                st.toast("Copié dans le presse-papier !")
    else:
        st.warning("⚠️ Aucune donnée trouvée. Vérifiez que votre tableau Google Sheets n'est pas vide.")

# ==========================================
# ONGLET 2 : DOCUMENTS PDF & DÉMARCHES
# ==========================================
with tab2:
    st.header("📚 Bibliothèque de documents")
    st.info("Retrouvez ici les documents officiels mis à jour (Réforme Mars 2026).")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("📋 Fiches de préconisation")
        with st.container(border=True):
            st.write("**Fiche d'évaluation des besoins**")
            st.link_button("📥 Télécharger PDF", "https://drive.google.com/file/d/1aEwrr1jAEMQE1pEiOUVs3ShwIXTKYDJ8/view")
        
        with st.container(border=True):
            st.write("**Fiche de préconisation technique**")
            st.link_button("📥 Télécharger PDF", "https://drive.google.com/file/d/1aEwrr1jAEMQE1pEiOUVs3ShwIXTKYDJ8/view")

    with col_b:
        st.subheader("📑 Démarches & Guides")
        with st.container(border=True):
            st.write("**Guide des démarches administratives**")
            st.link_button("📥 Voir le guide", "https://drive.google.com/file/d/1TXF4AiB_U9cwE1_56HoVrsCIE-RGZKLo/view")
            
        with st.container(border=True):
            st.write("**Tableau récapitulatif des classes**")
            st.link_button("📥 Ouvrir le document", "https://drive.google.com/file/d/1JZ97O8moGiemndSrMr-DNEUymjgeYi2V/view")

    st.markdown("---")
    st.warning("⚠️ **Rappel :** Cette application est un outil d'aide. Référez-vous toujours aux textes officiels de la Sécurité Sociale.")
