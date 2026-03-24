import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide")

# --- LECTURE ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

try:
    df = pd.read_csv(SHEET_URL)
    df.columns = [str(c).strip().upper() for c in df.columns]
except Exception as e:
    st.error(f"Erreur de lecture du Google Sheet : {e}")
    st.stop()

st.title("🦽 Assistant Réforme VPH 2026")

# --- RECHERCHE ---
recherche = st.text_input("🔍 Rechercher un modèle (ex: TDX, Action...)", "").strip()

if recherche:
    df = df[df.astype(str).apply(lambda x: x.str.contains(recherche, case=False)).any(axis=1)]

# --- AFFICHAGE DES FICHES ---
cols = st.columns(2)

for idx, (i, row) in enumerate(df.iterrows()):
    with cols[idx % 2]:
        with st.container(border=True):
            st.subheader(f"{row.get('FABRICANT', '')} - {row.get('MODELE', '')}")
            
            c1, c2 = st.columns([1, 1.3])
            
            with c1:
                # --- PHOTO ---
                photo_link = ""
                for col in df.columns:
                    if "PHOTO" in col:
                        val = str(row[col]).strip()
                        if val.lower().startswith("http"):
                            photo_link = val
                            break
                
                if photo_link:
                    st.image(photo_link, use_container_width=True)
                else:
                    st.info("📷 Image non dispo")
                
            with c2:
                # --- INFOS TECHNIQUES ---
                categorie = row.get('CATEGORIE', '-')
                st.write(f"**Catégorie :** {categorie}")

                # --- LIEN FICHE TECHNIQUE (TEXTE CLIQUABLE) ---
                pdf_link = ""
                if "FICHE TECHNIQUE" in df.columns:
                    pdf_link = str(row["FICHE TECHNIQUE"]).strip()
                
                if not pdf_link.lower().startswith("http"):
                    for val in row:
                        if str(val).lower().startswith("http") and ("drive.google" in str(val).lower() or ".pdf" in str(val).lower()):
                            pdf_link = str(val).strip()
                            break
                
                if pdf_link.lower().startswith("http"):
                    # On affiche un lien hypertexte classique
                    st.markdown(f"📎 [**Ouvrir la Fiche Technique (PDF)**]({pdf_link})")
                else:
                    st.caption("⚠️ Aucune fiche liée")

                st.divider()

                st.write(f"**Référence :** `{row.get('CODE_REF', 'N/A')}`")
                st.write(f"**LPPR :** `{row.get('CODE_LPPR', 'N/A')}`")
                st.write(f"**Châssis :** {row.get('CHASSIS', '-')}")
                st.write(f"**Dossier :** {row.get('DOSSIER', '-')}")
                
                libelle = row.get('LIBELLE_PRESCRIPTION', '')
                if libelle and str(libelle).lower() != "non spécifié":
                    with st.expander("📝 Voir le libellé"):
                        st.write(libelle)

st.divider()
st.caption("Note : Si le lien ne s'ouvre pas, vérifiez que le lien dans Google Sheet commence bien par 'https://'")
