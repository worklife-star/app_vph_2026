import streamlit as st
import pandas as pd
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide")

# --- LECTURE ---
# Utilisation du lien Google Sheets CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Nettoyage strict des noms de colonnes
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return None

df_raw = load_data()

st.title("🦽 Assistant Réforme VPH 2026")

# --- RECHERCHE ---
recherche = st.text_input("🔍 Rechercher un modèle...", "").strip()

if df_raw is not None:
    df = df_raw.copy()
    if recherche:
        df = df[df.astype(str).apply(lambda x: x.str.contains(recherche, case=False)).any(axis=1)]

    # --- AFFICHAGE ---
    cols = st.columns(2)
    for idx, (i, row) in enumerate(df.iterrows()):
        with cols[idx % 2]:
            with st.container(border=True):
                st.subheader(f"{row.get('FABRICANT', '')} - {row.get('MODELE', '')}")
                
                c1, c2 = st.columns([1, 1.3])
                
                with c1:
                    # Photo
                    photo = str(row.get('LIEN PHOTO', '')).strip()
                    if photo.lower().startswith("http"):
                        st.image(photo, use_container_width=True)
                    else:
                        st.info("📷 Image non dispo")
                
                with c2:
                    # Catégorie
                    st.write(f"**Catégorie :** {row.get('CATEGORIE', '-')}")

                    # --- GESTION DU LIEN PDF (CORRIGÉE) ---
                    pdf_link = str(row.get('FICHE TECHNIQUE', '')).strip()
                    
                    if pdf_link.lower().startswith("http"):
                        # On "nettoie" l'URL pour gérer les caractères spéciaux comme %7B
                        clean_url = urllib.parse.unquote(pdf_link)
                        clean_url = urllib.parse.quote(clean_url, safe=':/?&=_-%')
                        
                        # Affichage en lien bleu gras très visible
                        st.markdown(f"🔗 [**CLIQUEZ ICI POUR LE PDF**]({clean_url})")
                    else:
                        st.caption("⚠️ PDF non renseigné")

                    st.divider()
                    st.write(f"**Référence :** `{row.get('CODE_REF', 'N/A')}`")
                    st.write(f"**LPPR :** `{row.get('CODE_LPPR', 'N/A')}`")
                    
                    libelle = row.get('LIBELLE_PRESCRIPTION', '')
                    if libelle and str(libelle).lower() != "non spécifié":
                        with st.expander("📝 Libellé"):
                            st.write(libelle)

st.divider()
st.caption("Note : Si le lien ne s'ouvre toujours pas, vérifiez que votre navigateur ne bloque pas les fenêtres surgissantes.")
