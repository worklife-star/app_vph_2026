import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Assistant Réforme VPH", layout="wide")

# TITRE
st.title("🦽 Assistant Sélection Fauteuils Roulants (Réforme 2026)")
st.markdown("---")

# LIEN VERS VOTRE GOOGLE SHEET
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=600) 
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df = df.replace(["Non spécifié", "null", "nan"], "")
        return df
    except Exception as e:
        return None

data = load_data()

if data is not None:
    # --- BARRE LATÉRALE (FILTRES) ---
    st.sidebar.header("🔍 Filtres de sélection")
    
    # 1. Recherche textuelle globale
    recherche = st.sidebar.text_input("Recherche rapide (Modèle, LPPR, Ref...)")
    
    # 2. Filtre par Référence (CODE_REF)
    ref_list = []
    if "CODE_REF" in data.columns:
        ref_list = sorted([str(x) for x in data["CODE_REF"].unique() if x != ""])
    ref_choice = st.sidebar.multiselect("Référence Produit (CODE_REF)", ref_list)
    
    # 3. Autres filtres
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
                    st.write(f"**Prescripteur :** {row.get('PRESCRIPTEUR', '')}")
                
                with st.expander("📝 Libellé de prescription"):
                    libelle = row.get('LIBELLE_PRESCRIPTION', '')
                    if libelle:
                        st.write(libelle)
                        if st.button("Copier le libellé", key=f"cp_{idx}"):
                            st.copy_to_clipboard(libelle)
                            st.toast("Copié !")
                    else:
                        st.write("À compléter dans le Google Sheet.")
else:
    st.error("⚠️ Impossible de lire le Google Sheet. Vérifiez qu'il est bien 'Publié sur le Web' au format CSV.")
