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
    </style>
    """, unsafe_allow_html=True)

# --- FONCTION DE COULEUR PAR CATÉGORIE ---
def get_cat_color(categorie):
    cat = str(categorie).upper()
    if "MANUEL" in cat: return "#0288d1"
    if "ÉLECTRIQUE" in cat or "ELECTRIQUE" in cat: return "#f57c00"
    if "SPORT" in cat: return "#388e3c"
    if "ENFANT" in cat: return "#d32f2f"
    return "#9e9e9e"

# --- CHARGEMENT DES DONNÉES ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=10) # Réduit à 10s pour vos tests
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        
        # --- SOLUTION : NORMALISATION DES COLONNES ---
        # Supprime les espaces autour des noms et met tout en majuscules
        df.columns = df.columns.str.strip().str.upper()
        
        df = df.dropna(how='all')
        if "MODELE" in df.columns:
            df = df[df["MODELE"].notna() & (df["MODELE"] != "")]
        
        df = df.replace(["Non spécifié", "null", "nan", "NaN"], "")
        paris_tz = pytz.timezone('Europe/Paris')
        now = datetime.now(paris_tz).strftime("%H:%M")
        return df, now
    except Exception as e:
        st.error(f"Erreur : {e}")
        return None, None

data, last_update = load_data()

# --- TITRE PRINCIPAL ---
st.title("🦽 Assistant Réforme VPH 2026")

tab1, tab2 = st.tabs(["🔎 CATALOGUE VPH", "📂 DOCUMENTS & DÉMARCHES"])

with tab1:
    if data is not None and not data.empty:
        # Zone de filtres
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            recherche = st.text_input("📝 Recherche libre :", placeholder="Modèle, Marque...")
            cat_list = sorted([x for x in data["CATEGORIE"].unique() if str(x) != ""]) if "CATEGORIE" in data.columns else []
            cat_choice = st.multiselect("⚙️ Type de matériel :", cat_list)
        with col2:
            fab_list = sorted([x for x in data["FABRICANT"].unique() if str(x) != ""]) if "FABRICANT" in data.columns else []
            fab_choice = st.multiselect("🏭 Fabricant :", fab_list)
        st.markdown('</div>', unsafe_allow_html=True)

        # Filtrage
        df_f = data.copy()
        if recherche:
            mask = df_f.astype(str).apply(lambda x: x.str.contains(recherche, case=False)).any(axis=1)
            df_f = df_f[mask]
        if cat_choice: df_f = df_f[df_f["CATEGORIE"].isin(cat_choice)]
        if fab_choice: df_f = df_f[df_f["FABRICANT"].isin(fab_choice)]

        # Affichage
        cols = st.columns(2)
        for idx, (_, row) in enumerate(df_f.iterrows()):
            cat_color = get_cat_color(row.get('CATEGORIE', ''))
            
            with cols[idx % 2]:
                # En-tête coloré
                st.markdown(f"""
                    <div style="border-left: 8px solid {cat_color}; padding: 10px 15px; border-radius: 10px; background-color: #ffffff; border: 1px solid #eee; border-left: 8px solid {cat_color}; margin-bottom: 0px;">
                        <h3 style="margin:0;">{row.get('FABRICANT', '')} - {row.get('MODELE', '')}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.container(border=True):
                    c1, c2 = st.columns([1, 1.5])
                    with c1:
                        # Image
                        img = row.get('LIEN PHOTO', '')
                        if str(img).startswith('http'):
                            st.image(img, use_container_width=True)
                        else:
                            st.info("📷 Pas d'image")
                        
                        # --- SOLUTION BOUTON FICHE TECHNIQUE ---
                        # On force la recherche de la colonne même si le nom est un peu différent
                        ft_url = row.get('FICHE TECHNIQUE', '')
                        if str(ft_url).startswith('http'):
                            st.link_button("📄 FICHE TECHNIQUE", str(ft_url).strip(), use_container_width=True, type="primary")
                        else:
                            st.caption("Fiche non dispo")

                    with c2:
                        st.write(f"**Réf :** `{row.get('CODE_REF', 'N/A')}`")
                        st.write(f"**LPPR :** `{row.get('CODE_LPPR', 'N/A')}`")
                        st.markdown(f"**Châssis :** {row.get('CHASSIS', '-')}")
                        st.markdown(f"**Dossier :** {row.get('DOSSIER', '-')}")
                        st.markdown(f"**Catégorie :** {row.get('CATEGORIE', 'N/A')}")
                    
                    libelle = row.get('LIBELLE_PRESCRIPTION', '')
                    if libelle:
                        with st.expander("📝 Libellé"):
                            st.write(libelle)
                            if st.button("Copier", key=f"cp_{idx}"):
                                st.copy_to_clipboard(libelle)
                                st.toast("Copié !")
    else:
        st.warning("Aucune donnée. Vérifiez votre Google Sheet.")

# --- ONGLET 2 ---
with tab2:
    st.header("📚 Documents")
    st.link_button("📥 Fiche d'évaluation", "https://drive.google.com/file/d/1aEwrr1jAEMQE1pEiOUVs3ShwIXTKYDJ8/view")
