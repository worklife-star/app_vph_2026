import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Assistant Réforme VPH", layout="wide")

# TITRE DE L'APPLICATION
st.title("🦽 Assistant Sélection Fauteuils Roulants (Réforme 2026)")
st.markdown("---")

# --- VOTRE LIEN CORRECT ET VÉRIFIÉ ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=600) 
def load_data():
    # On force le chargement et on gère les erreurs de lecture
    df = pd.read_csv(SHEET_URL)
    df = df.replace(["Non spécifié", "null", "nan"], "")
    return df

try:
    data = load_data()

    # BARRE LATÉRALE (FILTRES)
    st.sidebar.header("🔍 Filtres de sélection")
    
    recherche = st.sidebar.text_input("Rechercher un modèle ou un code...")
    
    # Filtre Catégorie (Manuel / Électrique)
    col_cat = "CATEGORIE" if "CATEGORIE" in data.columns else data.columns[0]
    categories = st.sidebar.multiselect("Type de matériel", options=sorted(data[col_cat].unique()))
    
    fabricant = st.sidebar.multiselect("Fabricant", options=sorted(data["FABRICANT"].unique()))
    classe = st.sidebar.multiselect("Classe", options=sorted(data["CLASSE"].unique()))

    # FILTRAGE DES DONNÉES
    df_filtered = data.copy()
    
    if recherche:
        df_filtered = df_filtered[df_filtered.apply(lambda row: recherche.lower() in row.astype(str).str.lower().values, axis=1)]
    if categories:
        df_filtered = df_filtered[df_filtered[col_cat].isin(categories)]
    if fabricant:
        df_filtered = df_filtered[df_filtered["FABRICANT"].isin(fabricant)]
    if classe:
        df_filtered = df_filtered[df_filtered["CLASSE"].isin(classe)]

    # AFFICHAGE
    st.write(f"**{len(df_filtered)}** modèles disponibles.")

    cols = st.columns(2)
    for idx, row in df_filtered.iterrows():
        with cols[idx % 2]:
            with st.container(border=True):
                st.subheader(f"{row['FABRICANT']} - {row['MODELE']}")
                c1, c2 = st.columns([1, 2])
                with c1:
                    if 'LIEN PHOTO' in row and str(row['LIEN PHOTO']).startswith('http'):
                        st.image(row['LIEN PHOTO'], use_container_width=True)
                    else:
                        st.info("📷 Image")
                with c2:
                    st.write(f"**LPPR :** `{row['CODE_LPPR']}`")
                    st.write(f"**Prescripteur :** {row['PRESCRIPTEUR']}")
                
                with st.expander("📝 Libellé de prescription"):
                    libelle = row['LIBELLE_PRESCRIPTION']
                    if libelle and libelle != "":
                        st.write(libelle)
                        if st.button("Copier", key=f"copy_{idx}"):
                            st.copy_to_clipboard(libelle)
                            st.toast("Copié !")
                    else:
                        st.write("À compléter dans le Google Sheet.")

except Exception as e:
    st.error("⚠️ Connexion impossible au Google Sheet.")
    st.write("Vérifiez que le fichier est bien 'Publié sur le web' au format CSV.")
    # On affiche l'erreur technique pour vous aider
    st.exception(e)
