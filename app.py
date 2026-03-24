import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# --- CHARGEMENT DES DONNÉES ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Nettoyage automatique des noms de colonnes
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return None

df_raw = load_data()

# --- INTERFACE ---
st.title("🦽 Assistant Réforme VPH 2026")
recherche = st.text_input("🔍 Rechercher un modèle (ex: Action, TDX, Kuschall...)", "").strip()

if df_raw is not None:
    df = df_raw.copy()
    if recherche:
        mask = df.astype(str).apply(lambda x: x.str.contains(recherche, case=False)).any(axis=1)
        df = df[mask]

    st.write(f"💡 **{len(df)}** modèles trouvés.")

    # --- GRILLE D'AFFICHAGE ---
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

                    # --- BOUTON PDF (METHODE ANTI-RECHARGEMENT) ---
                    pdf_link = str(row.get('FICHE TECHNIQUE', '')).strip()
                    
                    if pdf_link.lower().startswith("http"):
                        # On crée un bouton HTML dans un composant isolé
                        html_button = f"""
                        <div style="margin-top:5px;">
                            <a href="{pdf_link}" target="_blank" rel="noopener noreferrer" 
                               style="text-decoration:none; background-color:#0288d1; color:white; 
                               padding:8px 15px; border-radius:5px; font-family:sans-serif; 
                               font-weight:bold; display:inline-block; font-size:14px;">
                               📄 VOIR FICHE TECHNIQUE (PDF)
                            </a>
                        </div>
                        """
                        # Le height=45 permet de laisser juste assez de place pour le bouton
                        components.html(html_button, height=45)
                    else:
                        st.caption("⚠️ Aucune fiche PDF")

                    st.divider()

                    # Infos techniques
                    st.write(f"**Référence :** `{row.get('CODE_REF', 'N/A')}`")
                    st.write(f"**LPPR :** `{row.get('CODE_LPPR', 'N/A')}`")
                    st.write(f"**Châssis :** {row.get('CHASSIS', '-')}")
                    
                    # Libellé
                    libelle = row.get('LIBELLE_PRESCRIPTION', '')
                    if libelle and str(libelle).lower() != "non spécifié":
                        with st.expander("📝 Libellé"):
                            st.write(libelle)
else:
    st.error("Impossible de charger les données.")
