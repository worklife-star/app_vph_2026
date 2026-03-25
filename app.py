import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# --- CHARGEMENT DES DONNÉES ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
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

    cols = st.columns(2)

    for idx, (i, row) in enumerate(df.iterrows()):
        with cols[idx % 2]:
            with st.container(border=True):
                st.subheader(f"{row.get('FABRICANT', '')} - {row.get('MODELE', '')}")

                c1, c2 = st.columns([1, 1.3])

                with c1:
                    photo = str(row.get('LIEN PHOTO', '')).strip()
                    if photo.lower().startswith("http"):
                        st.image(photo, use_container_width=True)
                    else:
                        st.info("📷 Image non dispo")

                with c2:
                    st.write(f"**Catégorie :** {row.get('CATEGORIE', '-')}")

                    # ✅ CORRECTION : st.link_button() remplace components.html()
                    pdf_link = str(row.get('FICHE TECHNIQUE', '')).strip()
                    if pdf_link.lower().startswith("http"):
                        st.link_button("📄 VOIR FICHE TECHNIQUE (PDF)", pdf_link)
                    else:
                        st.caption("⚠️ Aucune fiche PDF")

                    st.divider()
                    st.write(f"**Référence :** `{row.get('CODE_REF', 'N/A')}`")
                    st.write(f"**LPPR :** `{row.get('CODE_LPPR', 'N/A')}`")
                    st.write(f"**Châssis :** {row.get('CHASSIS', '-')}")

                    libelle = row.get('LIBELLE_PRESCRIPTION', '')
                    if libelle and str(libelle).lower() != "non spécifié":
                        with st.expander("📝 Libellé"):
                            st.write(libelle)
else:
    st.error("Impossible de charger les données.")
