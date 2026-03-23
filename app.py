import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Assistant Réforme VPH", layout="wide")

# TITRE DE L'APPLICATION
st.title("🦽 Assistant Sélection Fauteuils Roulants (Réforme 2026)")
st.markdown("---")

# CHARGEMENT DES DONNÉES
# Remplacez l'URL ci-dessous par le lien CSV que vous avez copié à l'étape 1
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=600) # Mise à jour auto toutes les 10 min
def load_data():
    df = pd.read_csv(SHEET_URL)
    # Nettoyage simple pour le rendu pro
    df = df.replace("Non spécifié", "")
    return df

try:
    data = load_data()

    # BARRE LATÉRALE (FILTRES)
    st.sidebar.header("🔍 Filtres de sélection")
    
    recherche = st.sidebar.text_input("Rechercher un modèle ou un code...")
    
    fabricant = st.sidebar.multiselect("Fabricant", options=sorted(data["FABRICANT"].unique()))
    classe = st.sidebar.multiselect("Classe", options=sorted(data["CLASSE"].unique()))
    usage = st.sidebar.multiselect("Usage", options=sorted(data["USAGE"].dropna().unique()))

    # FILTRAGE DES DONNÉES
    df_filtered = data.copy()
    if recherche:
        df_filtered = df_filtered[df_filtered.apply(lambda row: recherche.lower() in row.astype(str).str.lower().values, axis=1)]
    if fabricant:
        df_filtered = df_filtered[df_filtered["FABRICANT"].isin(fabricant)]
    if classe:
        df_filtered = df_filtered[df_filtered["CLASSE"].isin(classe)]
    if usage:
        df_filtered = df_filtered[df_filtered["USAGE"].isin(usage)]

    # AFFICHAGE DES RÉSULTATS
    st.write(f"**{len(df_filtered)}** modèles correspondent à vos critères.")

    # Création de colonnes pour un rendu "Catalogue"
    cols = st.columns(2)
    for idx, row in df_filtered.iterrows():
        with cols[idx % 2]:
            with st.container(border=True):
                st.subheader(f"{row['FABRICANT']} - {row['MODELE']}")
                
                col_img, col_info = st.columns([1, 2])
                
                with col_img:
                    if row['LIEN PHOTO'] and str(row['LIEN PHOTO']).startswith('http'):
                        st.image(row['LIEN PHOTO'], use_container_width=True)
                    else:
                        st.info("📷 Photo à venir")
                
                with col_info:
                    st.write(f"**Code LPPR :** `{row['CODE_LPPR']}`")
                    st.write(f"**Prescripteur :** {row['PRESCRIPTEUR']}")
                    st.write(f"**Prise en charge :** {row['TARIF_PRIS_EN_CHARGE']} €")
                
                with st.expander("📝 Libellé de prescription (Copier)"):
                    st.code(row['LIBELLE_PRESCRIPTION'] if row['LIBELLE_PRESCRIPTION'] else "Libellé non encore saisi.")
                
                if row['FICHE TECHNIQUE'] and str(row['FICHE TECHNIQUE']).startswith('http'):
                    st.link_button("📄 Voir la Fiche Technique", row['FICHE TECHNIQUE'])

except Exception as e:
    st.error("Erreur lors de la connexion au tableau. Vérifiez que le tableau est bien 'Publié sur le web'.")
