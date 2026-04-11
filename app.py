import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# --- CSS PERSONNALISÉ ---
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #fafafa 50%, #f0f8f4 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a2744 0%, #0f3460 100%) !important;
        border-right: none !important;
    }
    [data-testid="stSidebar"] * {
        color: #e8edf8 !important;
    }
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #ffffff !important;
        font-family: 'DM Serif Display', serif !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15) !important;
    }
    [data-testid="stSidebar"] .stCaption {
        color: rgba(255,255,255,0.45) !important;
        font-size: 0.7rem !important;
    }

    /* Sidebar buttons */
    [data-testid="stSidebar"] .stLinkButton a {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebar"] .stLinkButton a:hover {
        background: rgba(255,255,255,0.2) !important;
        border-color: rgba(255,255,255,0.4) !important;
        transform: translateX(3px) !important;
    }

    /* Titre principal */
    h1 {
        font-family: 'DM Serif Display', serif !important;
        font-size: 2.2rem !important;
        color: #1a2744 !important;
        letter-spacing: -0.5px;
    }

    /* Sous-titres cartes */
    h3 {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #1a2744 !important;
    }

    /* Champ de recherche */
    .stTextInput input {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        background: white !important;
        transition: border-color 0.2s !important;
    }
    .stTextInput input:focus {
        border-color: #0f3460 !important;
        box-shadow: 0 0 0 3px rgba(15,52,96,0.1) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: white !important;
    }

    /* Bouton reset */
    .stButton > button {
        border-radius: 10px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: white !important;
        color: #1a2744 !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: #1a2744 !important;
        color: white !important;
        border-color: #1a2744 !important;
    }

    /* Cartes modèles */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: white !important;
        border-radius: 16px !important;
        border: 1px solid #e8edf8 !important;
        box-shadow: 0 2px 12px rgba(26,39,68,0.06) !important;
        transition: box-shadow 0.2s, transform 0.2s !important;
        overflow: hidden !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 8px 30px rgba(26,39,68,0.12) !important;
        transform: translateY(-2px) !important;
    }

    /* Badges infos */
    code {
        background: #eef2ff !important;
        color: #0f3460 !important;
        border-radius: 6px !important;
        font-size: 0.8rem !important;
        padding: 2px 8px !important;
        font-family: 'DM Sans', monospace !important;
    }

    /* Bouton fiche technique */
    .stLinkButton a {
        background: #0f3460 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 8px 14px !important;
        transition: all 0.2s !important;
    }
    .stLinkButton a:hover {
        background: #1a2744 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(15,52,96,0.3) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #0f3460 !important;
        background: #f8faff !important;
        border-radius: 8px !important;
    }

    /* Divider */
    hr {
        border-color: #eef2ff !important;
        margin: 8px 0 !important;
    }

    /* Info image */
    .stAlert {
        border-radius: 10px !important;
        font-size: 0.8rem !important;
    }

    /* Caption */
    .stCaption {
        color: #94a3b8 !important;
        font-size: 0.75rem !important;
    }

    /* Compteur résultats */
    .result-count {
        background: #eef2ff;
        color: #0f3460;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Section filtres */
    .filter-section {
        background: white;
        border-radius: 14px;
        padding: 16px;
        border: 1px solid #e8edf8;
        margin-bottom: 20px;
        box-shadow: 0 1px 6px rgba(26,39,68,0.04);
    }
</style>
""", unsafe_allow_html=True)

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

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.markdown("## 📂 Documents utiles")
    st.markdown("Téléchargez les documents officiels pour vos prescriptions.")
    st.divider()

    docs = [
        ("📋 Fiche de préconisation",    "1aEwrr1jAEMQE1pEiOUVs3ShwIXTKYDJ8"),
        ("📝 Évaluation des besoins",    "1OXc5N-rPpOAzI3r1F8Ov887mn_k75qoD"),
        ("🪑 VPH par catégorie",         "1_vMX4OU5tqm5OU_YtNyUel2SatFQ_VyJ"),
        ("👨‍⚕️ Qui peut prescrire ?",     "1ZRKYZhsRx_5SiUNOAMhoRC8EtesPx9ja"),
    ]
    for label, file_id in docs:
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        st.link_button(label, url, use_container_width=True)

    st.divider()
    st.caption("🔄 Données actualisées toutes les 60 s")

# --- INTERFACE PRINCIPALE ---
st.title("🦽 Assistant Réforme VPH 2026")
st.markdown("Retrouvez rapidement les fauteuils roulants, leurs codes LPPR et leurs conditions de prescription.")
st.markdown("")

if df_raw is not None:
    df = df_raw.copy()

    # --- RECHERCHE ---
    recherche = st.text_input("🔍 Rechercher un modèle, fabricant, code…", "").strip()

    # --- FILTRES ---
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown("**🎛️ Filtres**")
    f1, f2, f3, f4, f5 = st.columns(5)

    def get_options(col):
        if col in df_raw.columns:
            vals = sorted([v for v in df_raw[col].dropna().astype(str).unique() if v.lower() != "non spécifié"])
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
    st.markdown('</div>', unsafe_allow_html=True)

    # --- APPLICATION DES FILTRES ---
    if recherche:
        mask = df.astype(str).apply(lambda x: x.str.contains(recherche, case=False, na=False)).any(axis=1)
        df = df[mask]

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

    # --- RESET + COMPTEUR ---
    col_reset, col_count = st.columns([1, 4])
    with col_reset:
        if st.button("🔄 Réinitialiser"):
            st.rerun()
    with col_count:
        st.markdown(f'<div class="result-count">💡 {len(df)} modèle{"s" if len(df) > 1 else ""} trouvé{"s" if len(df) > 1 else ""}</div>', unsafe_allow_html=True)

    st.markdown("")

    # --- GRILLE ---
    if df.empty:
        st.warning("Aucun résultat. Modifiez les filtres ou la recherche.")
    else:
        cols = st.columns(2)
        for idx, (i, row) in enumerate(df.iterrows()):
            col = cols[idx % 2]
            with col:
                with st.container(border=True):
                    fabricant = str(row.get("FABRICANT", ""))
                    modele = str(row.get("MODELE", ""))
                    st.subheader(f"{fabricant} — {modele}")

                    c1, c2 = st.columns([1, 1.3])

                    with c1:
                        photo = str(row.get("LIEN_PHOTO", "")).strip()
                        if photo.lower().startswith("http"):
                            if "drive.google.com/file/d/" in photo:
                                file_id = photo.split("/d/")[1].split("/")[0]
                                photo = f"https://drive.google.com/uc?export=view&id={file_id}"
                            st.image(photo, use_container_width=True)
                        else:
                            st.info("📷 Image non dispo")

                    with c2:
                        # Infos générales
                        categorie = str(row.get("CATEGORIE", "-"))
                        sous_type = str(row.get("SOUS_TYPE", "-"))
                        classe = str(row.get("CLASSE", "-"))

                        if categorie not in ["-", "nan"]:
                            st.write(f"**Catégorie :** {categorie}")
                        if sous_type not in ["-", "nan"]:
                            st.write(f"**Sous-type :** {sous_type}")
                        if classe not in ["-", "nan"]:
                            st.write(f"**Classe :** {classe}")

                        st.divider()

                        # Codes
                        st.write(f"**Référence :** `{row.get('CODE_REF', 'N/A')}`")
                        lppr_am = str(row.get("CODE_LPPR_ASSURANCE_MALADIE", ""))
                        if lppr_am and lppr_am.lower() not in ["nan", ""]:
                            st.write(f"**LPPR AM :** `{lppr_am}`")
                        lppr_ind = str(row.get("CODE_LPPR_INDIVIDUEL_FOURNISSEUR", ""))
                        if lppr_ind and lppr_ind.lower() not in ["nan", ""]:
                            st.write(f"**LPPR Indiv. :** `{lppr_ind}`")

                        chassis = str(row.get("CHASSIS", "-"))
                        if chassis not in ["-", "nan"]:
                            st.write(f"**Châssis :** {chassis}")

                        usage = str(row.get("USAGE", ""))
                        if usage and usage.lower() not in ["nan", "non spécifié", ""]:
                            st.write(f"**Usage :** {usage}")

                        poids = str(row.get("POIDS", ""))
                        if poids and poids.lower() not in ["nan", "non spécifié", ""]:
                            st.write(f"**⚖️ Poids :** {poids}")

                        tarif = str(row.get("TARIF_PRIS_EN_CHARGE", ""))
                        if tarif and tarif.lower() not in ["nan", "non spécifié", ""]:
                            st.write(f"**💶 Tarif pris en charge :** {tarif}")

                        st.divider()

                        # Prescription + Libellé + Fiche regroupés
                        prescripteur = str(row.get("PRESCRIPTEUR", ""))
                        if prescripteur and prescripteur.lower() not in ["non spécifié", "nan", ""]:
                            st.write(f"**👨‍⚕️ Prescripteur :** {prescripteur}")

                        libelle = str(row.get("LIBELLE_PRESCRIPTION", ""))
                        if libelle and libelle.lower() not in ["non spécifié", "nan", ""]:
                            with st.expander("📝 Libellé prescription"):
                                st.write(libelle)

                        pdf_link = str(row.get("FICHE_TECHNIQUE", "")).strip()
                        if pdf_link.lower().startswith("http"):
                            st.link_button("📄 Fiche technique (PDF)", pdf_link)
                        else:
                            st.caption("⚠️ Aucune fiche PDF")

                        descripteurs = str(row.get("DESCRIPEURS", ""))
                        if descripteurs and descripteurs.lower() not in ["non spécifié", "nan", ""]:
                            with st.expander("🏷️ Descripteurs"):
                                st.write(descripteurs)

else:
    st.error("Impossible de charger les données.")
