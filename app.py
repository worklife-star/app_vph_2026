import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Configuration de la page
st.set_page_config(page_title="Expert VPH 2026", layout="wide")

# --- STYLE PERSONNALISÉ (CSS) ---
st.markdown("""
    <style>
    /* Style pour l'encadré des filtres */
    .filter-box {
        background-color: #e1f5fe;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #0288d1;
        margin-bottom: 25px;
    }
    /* Rendre les titres de filtres plus gras */
    .stMultiSelect label, .stTextInput label {
        font-weight: bold !important;
        color: #01579b !important;
    }
    </style>
    """, unsafe_allow_html=True)

# TITRE
st.title("🦽 Assistant Sélection Fauteuils Roulants")

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

if last_update:
    st.caption(f"✅ Dernière synchro : {last_update}")

# --- ZONE DE FILTRES BIEN VISIBLE ---
st.markdown('<div class="filter-box">', unsafe_allow_html=True)
st.subheader("🔍 RECHERCHE & FILTRES")

col1, col2 = st.columns(2)
with col1:
    recherche = st.text_input("📝 Tapez un nom, un code ou une marque :", placeholder="Ex: Invacare...")
    cat_list = sorted(data["CATEGORIE"].unique()) if data is not None and "CATEGORIE" in data.columns else []
    cat_choice = st.multiselect("⚙️ Type de matériel :", cat_list)

with col2:
    ref_list = sorted([str(x) for x in data["CODE_REF"].unique() if x != ""]) if data is not None and "CODE_REF" in data.columns else []
    ref_choice = st.multiselect("🔢 Référence Produit (CODE_REF) :", ref_list)
    fab_list = sorted(data["FABRICANT"].unique()) if data is not None and "FABRICANT" in data.columns else []
    fab_choice = st.multiselect("🏭 Fabricant :", fab_list)

st.markdown('</div>', unsafe_allow_html=True)

# --- LOGIQUE DE FILTRAGE ---
if data is not None:
    df = data.copy()
    if recherche:
        df = df[df.apply(lambda row: recherche.lower() in row.astype(str).str.lower().values, axis=1)]
    if ref_choice:
        df = df[df["CODE_REF"].astype(str).isin(ref_choice)]
    if cat_choice:
        df = df[df["CATEGORIE"].isin(cat_choice)]
    if fab_choice:
        df = df[df["FABRICANT"].isin(fab_choice)]

    st.write(f"💡 **{len(df)}** modèles correspondent à votre sélection.")
    st.markdown("---")

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
                        st.info("📷 Image à venir")
                with c2:
                    st.write(f"**Réf :** `{row.get('CODE_REF', 'N/A')}`")
                    st.write(f"**LPPR :** `{row.get('CODE_LPPR', '')}`")
                    st.write(f"**Prescripteur :** {row.get('PRESCRIPTEUR', '')}")
                
                with st.expander("📝 Libellé de prescription"):
                    libelle = row.get('LIBELLE_PRESCRIPTION', '')
                    if libelle:
                        st.write(libelle)
                        if st.button("Copier", key=f"cp_{idx}"):
                            st.copy_to_clipboard(libelle)
                            st.toast("Copié !")
                    else:
                        st.write("Libellé en cours de rédaction.")
else:
    st.error("Impossible de charger les données.")
