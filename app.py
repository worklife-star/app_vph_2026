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
        df.columns = [str(c).strip().upper().replace(" ", "_") for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return None

df_raw = load_data()

# --- INTERFACE ---
st.title("🦽 Assistant Réforme VPH 2026")

if df_raw is not None:
    df = df_raw.copy()

    # --- RECHERCHE TEXTUELLE ---
    recherche = st.text_input("🔍 Rechercher un modèle (ex: Action, TDX, Kuschall...)", "").strip()

    # --- FILTRES EN HAUT DE PAGE ---
    st.markdown("### 🎛️ Filtres")
    f1, f2, f3, f4, f5 = st.columns(5)

    def get_options(col):
        """Retourne les valeurs uniques triées d'une colonne, avec 'Tous' en premier."""
        if col in df_raw.columns:
            vals = sorted(df_raw[col].dropna().astype(str).unique().tolist())
            return ["Tous"] + vals
        return ["Tous"]

    with f1:
        filtre_categorie = st.selectbox("📁 Catégorie", get_options("CATEGORIE"))
    with f2:
        filtre_fabricant = st.selectbox("🏭 Fabricant", get_options("FABRICANT"))
    with f3:
        filtre_chassis = st.selectbox("🔩 Châssis", get_options("CHASSIS"))
    with f4:
        filtre_ref = st.selectbox("🔖 Code Réf.", get_options("CODE_REF"))
    with f5:
        filtre_sous_type = st.selectbox("📂 Sous-type", get_options("SOUS_TYPE"))

    # --- APPLICATION DE LA RECHERCHE ---
    if recherche:
        mask = df.astype(str).apply(lambda x: x.str.contains(recherche, case=False, na=False)).any(axis=1)
        df = df[mask]

    # --- APPLICATION DES FILTRES ---
    filtres = {
        "CATEGORIE": filtre_categorie,
        "FABRICANT": filtre_fabricant,
        "CHASSIS": filtre_chassis,
        "CODE_REF": filtre_ref,
        "SOUS_TYPE": filtre_sous_type,
    }
    for col, val in filtres.items():
        if val != "Tous" and col in df.columns:
            df = df[df[col].astype(str) == val]

    # --- BOUTON RESET ---
    if st.button("🔄 Réinitialiser les filtres"):
        st.rerun()

    st.write(f"💡 **{len(df)}** modèles trouvés.")
    st.divider()

    # --- GRILLE D'AFFICHAGE ---
    if df.empty:
        st.warning("Aucun résultat pour ces critères. Essayez de modifier les filtres.")
    else:
        cols = st.columns(2)
        for idx, (i, row) in enumerate(df.iterrows()):
            col = cols[idx % 2]
            with col:
                with st.container(border=True):
                    fabricant = str(row.get("FABRICANT", ""))
                    modele = str(row.get("MODELE", ""))
                    st.subheader(f"{fabricant} - {modele}")

                    c1, c2 = st.columns([1, 1.3])

                    with c1:
                        photo = str(row.get("LIEN_PHOTO", row.get("LIEN PHOTO", ""))).strip()
                        if photo.lower().startswith("http"):
                            st.image(photo, use_container_width=True)
                        else:
                            st.info("📷 Image non dispo")

                    with c2:
                        st.write(f"**Catégorie :** {row.get('CATEGORIE', '-')}")
                        st.write(f"**Sous-type :** {row.get('SOUS_TYPE', '-')}")

                        pdf_link = str(row.get("FICHE_TECHNIQUE", row.get("FICHE TECHNIQUE", ""))).strip()
                        if pdf_link.lower().startswith("http"):
                            st.link_button("📄 VOIR FICHE TECHNIQUE (PDF)", pdf_link)
                        else:
                            st.caption("⚠️ Aucune fiche PDF")

                        st.divider()
                        st.write(f"**Référence :** `{row.get('CODE_REF', 'N/A')}`")
                        st.write(f"**LPPR :** `{row.get('CODE_LPPR', 'N/A')}`")
                        st.write(f"**Châssis :** {row.get('CHASSIS', '-')}")

                        libelle = str(row.get("LIBELLE_PRESCRIPTION", ""))
                        if libelle and libelle.lower() not in ["non spécifié", "nan", ""]:
                            with st.expander("📝 Libellé"):
                                st.write(libelle)

else:
    st.error("Impossible de charger les données.")
