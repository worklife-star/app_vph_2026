import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Expert VPH 2026", layout="wide")

# 2. Lien vers ton Google Sheet (format CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

# 3. Chargement des données (on désactive le cache pour être sûr de voir les changements)
@st.cache_data(ttl=0)
def load_data():
    df = pd.read_csv(SHEET_URL)
    # On nettoie juste les espaces autour des noms de colonnes
    df.columns = [c.strip() for c in df.columns]
    return df

df = load_data()

st.title("🦽 Assistant Réforme VPH 2026")

# 4. Barre de recherche
recherche = st.text_input("🔍 Rechercher un modèle (ex: TDX, Action 2...)", "")

# 5. Filtrage
if recherche:
    df = df[df.astype(str).apply(lambda x: x.str.contains(recherche, case=False)).any(axis=1)]

# 6. Affichage des fiches
cols = st.columns(2)

for idx, row in df.iterrows():
    with cols[idx % 2]:
        with st.container(border=True):
            st.subheader(f"{row.get('FABRICANT', '')} - {row.get('MODELE', '')}")
            
            c1, c2 = st.columns([1, 1.5])
            
            with c1:
                # --- AFFICHAGE PHOTO ---
                photo = str(row.get('LIEN PHOTO', '')).strip()
                if photo.startswith('http'):
                    st.image(photo, use_container_width=True)
                else:
                    st.info("📷 Image non dispo")
                
                # --- BOUTON FICHE TECHNIQUE (JUSTE EN DESSOUS) ---
                # On récupère le lien PDF comme celui que tu m'as donné
                lien_pdf = str(row.get('FICHE TECHNIQUE', '')).strip()
                
                if lien_pdf.startswith('http'):
                    st.link_button("📄 FICHE TECHNIQUE", lien_pdf, use_container_width=True, type="primary")
                else:
                    st.caption("⚠️ Lien PDF manquant")

            with c2:
                # Autres infos
                st.write(f"**Référence :** {row.get('CODE_REF', 'N/A')}")
                st.write(f"**LPPR :** {row.get('CODE_LPPR', 'N/A')}")
                st.write(f"**Châssis :** {row.get('CHASSIS', '-')}")
                st.write(f"**Dossier :** {row.get('DOSSIER', '-')}")
                
                # Libellé de prescription
                libelle = row.get('LIBELLE_PRESCRIPTION', '')
                if libelle and libelle != "Non spécifié":
                    with st.expander("📝 Voir le libellé"):
                        st.write(libelle)
