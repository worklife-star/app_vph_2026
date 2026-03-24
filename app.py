
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# --- CHARGEMENT ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Nettoyage automatique des noms de colonnes (enlève espaces et met en majuscules)
        df.columns = df.columns.str.strip().str.upper()
        df = df.dropna(how='all')
        df = df.fillna("")
        
        paris_tz = pytz.timezone('Europe/Paris')
        now = datetime.now(paris_tz).strftime("%H:%M")
        return df, now
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return None, None

data, last_update = load_data()

# --- INTERFACE ---
st.title("🦽 Assistant Réforme VPH 2026")

if data is not None:
    # Recherche
    recherche = st.text_input("🔍 Rechercher un modèle :")
    
    df_f = data.copy()
    if recherche:
        mask = df_f.astype(str).apply(lambda x: x.str.contains(recherche, case=False)).any(axis=1)
        df_f = df_f[mask]

    # Grille
    cols = st.columns(2)
    for idx, (_, row) in enumerate(df_f.iterrows()):
        with cols[idx % 2]:
            # Utilisation de container pour séparer les fiches
            with st.container(border=True):
                st.subheader(f"{row.get('FABRICANT', '---')} - {row.get('MODELE', '---')}")
                
                c1, c2 = st.columns([1, 1.5])
                
                with c1:
                    # Affichage Image
                    img = str(row.get('LIEN PHOTO', '')).strip()
                    if img.startswith('http'):
                        st.image(img, use_container_width=True)
                    else:
                        st.info("📷 Pas d'image")
                    
                    # --- LE BOUTON FICHE TECHNIQUE (VERIFICATION FORCEE) ---
                    # On cherche la colonne "FICHE TECHNIQUE" ou "FICHETECHNIQUE"
                    ft_link = str(row.get('FICHE TECHNIQUE', row.get('FICHETECHNIQUE', ''))).strip()
                    
                    if ft_link.startswith('http'):
                        # BOUTON BLEU SI LIEN OK
                        st.link_button("📄 VOIR FICHE TECHNIQUE", ft_link, use_container_width=True, type="primary")
                    else:
                        # MESSAGE D'ERREUR ROUGE SI LIEN KO
                        st.error("🚫 Fiche non renseignée")

                with c2:
                    st.write(f"**Réf :** `{row.get('CODE_REF', 'N/A')}`")
                    st.write(f"**LPPR :** `{row.get('CODE_LPPR', 'N/A')}`")
                    st.write(f"**Châssis :** {row.get('CHASSIS', '-')}")
                    st.write(f"**Dossier :** {row.get('DOSSIER', '-')}")
                    st.caption(f"Catégorie : {row.get('CATEGORIE', 'N/A')}")
                
                # Libellé
                libelle = row.get('LIBELLE_PRESCRIPTION', '')
                if libelle:
                    with st.expander("📝 Libellé de prescription"):
                        st.write(libelle)
                        if st.button("Copier", key=f"cp_{idx}"):
                            st.copy_to_clipboard(libelle)
                            st.toast("Copié !")
