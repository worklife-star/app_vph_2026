import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# --- CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .filter-box { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #dee2e6; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f0f2f6; border-radius: 5px 5px 0px 0px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #0288d1 !important; color: white !important; }
    .card-header { padding: 10px 15px; border-radius: 10px 10px 0 0; background-color: #ffffff; border: 1px solid #eee; margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CHARGEMENT ET NETTOYAGE AGRESSIF ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=5) # Mise à jour quasi instantanée pour tes tests
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        
        # 1. On nettoie les noms de colonnes : tout en MAJUSCULES et on enlève TOUS les espaces
        # "FICHE TECHNIQUE" devient "FICHETECHNIQUE"
        df.columns = df.columns.str.replace(' ', '').str.upper().str.strip()
        
        # 2. On enlève les lignes vides
        df = df.dropna(how='all')
        
        # 3. On remplace les erreurs par du vide
        df = df.fillna("")
        df = df.replace(["Non spécifié", "null", "nan", "NaN", "None"], "")
        
        paris_tz = pytz.timezone('Europe/Paris')
        now = datetime.now(paris_tz).strftime("%H:%M")
        return df, now
    except Exception as e:
        st.error(f"Erreur technique : {e}")
        return None, None

data, last_update = load_data()

# --- COULEURS ---
def get_cat_color(cat):
    c = str(cat).upper()
    if "MANUEL" in c: return "#0288d1"
    if "ELECTRIQUE" in c or "ÉLECTRIQUE" in c: return "#f57c00"
    if "SPORT" in c: return "#388e3c"
    return "#9e9e9e"

# --- INTERFACE ---
st.title("🦽 Assistant Réforme VPH 2026")

tab1, tab2 = st.tabs(["🔎 CATALOGUE", "📂 DOCUMENTS"])

with tab1:
    if data is not None:
        # Barre de recherche
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        recherche = st.text_input("📝 Rechercher un modèle, une marque ou un composant :", placeholder="Ex: Invacare, Carbone, pliant...")
        st.markdown('</div>', unsafe_allow_html=True)

        # Filtrage
        df_f = data.copy()
        if recherche:
            mask = df_f.astype(str).apply(lambda x: x.str.contains(recherche, case=False)).any(axis=1)
            df_f = df_f[mask]

        # Affichage en Grille
        cols = st.columns(2)
        for idx, (_, row) in enumerate(df_f.iterrows()):
            color = get_cat_color(row.get('CATEGORIE', ''))
            
            with cols[idx % 2]:
                # Titre de la carte
                st.markdown(f"""
                    <div style="border-left: 8px solid {color}; padding: 10px 15px; border-radius: 10px; background-color: #ffffff; border: 1px solid #eee; margin-top: 20px;">
                        <h3 style="margin:0;">{row.get('FABRICANT', '---')} - {row.get('MODELE', '---')}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.container(border=True):
                    c1, c2 = st.columns([1, 1.5])
                    
                    with c1:
                        # Image
                        img = row.get('LIENPHOTO', '')
                        if str(img).startswith('http'):
                            st.image(img, use_container_width=True)
                        else:
                            st.info("📷 Image")
                        
                        # --- LE BOUTON FICHE TECHNIQUE (NOM DE COLONNE NETTOYÉ) ---
                        ft_url = row.get('FICHETECHNIQUE', '')
                        if str(ft_url).startswith('http'):
                            st.link_button("📄 FICHE TECHNIQUE", str(ft_url).strip(), use_container_width=True, type="primary")
                        else:
                            st.caption("🚫 Fiche technique absente")

                    with c2:
                        st.write(f"**Réf :** `{row.get('CODEREF', 'N/A')}`")
                        st.write(f"**LPPR :** `{row.get('CODELPPR', 'N/A')}`")
                        st.markdown(f"**Châssis :** {row.get('CHASSIS', '-')}")
                        st.markdown(f"**Dossier :** {row.get('DOSSIER', '-')}")
                        st.markdown(f"**Catégorie :** {row.get('CATEGORIE', 'N/A')}")
                    
                    # Libellé
                    libelle = row.get('LIBELLEPRESCRIPTION', '')
                    if libelle:
                        with st.expander("📝 Libellé de prescription"):
                            st.write(libelle)
                            if st.button("Copier", key=f"cp_{idx}"):
                                st.copy_to_clipboard(libelle)
                                st.toast("Copié !")

with tab2:
    st.header("📚 Documents de référence")
    st.link_button("📥 Fiche d'évaluation des besoins", "https://drive.google.com/file/d/1aEwrr1jAEMQE1pEiOUVs3ShwIXTKYDJ8/view")
    st.link_button("📥 Guide des démarches administratives", "https://drive.google.com/file/d/1TXF4AiB_U9cwE1_56HoVrsCIE-RGZKLo/view")
