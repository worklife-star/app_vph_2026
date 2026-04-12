import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expert VPH 2026", layout="wide", page_icon="🦽")

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700&display=swap');

/* ── base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F4F6FA; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: #0B1F4B !important;
    border-right: 4px solid #2563EB !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p { color: #E2E8F0 !important; font-size: 0.9rem !important; }
[data-testid="stSidebar"] h2 {
    color: #FFFFFF !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 1.15rem !important;
    letter-spacing: -0.3px;
    padding-bottom: 4px;
    border-bottom: 2px solid #2563EB;
    margin-bottom: 8px !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; margin: 14px 0 !important; }
[data-testid="stSidebar"] .stCaption p { color: rgba(255,255,255,0.45) !important; font-size:0.72rem !important; }
[data-testid="stSidebar"] .stLinkButton a {
    background: #1D4ED8 !important;
    border: none !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 10px 14px !important;
    box-shadow: 0 2px 8px rgba(29,78,216,0.35) !important;
    transition: background 0.18s, transform 0.18s, box-shadow 0.18s !important;
    display: block !important;
    text-align: left !important;
}
[data-testid="stSidebar"] .stLinkButton a:hover {
    background: #2563EB !important;
    transform: translateX(5px) !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.5) !important;
}

/* ── titres ── */
h1 { font-family:'Sora',sans-serif !important; color:#0B1F4B !important; font-size:2rem !important; letter-spacing:-0.5px; margin-bottom:4px !important; }
.subtitle { color:#475569; font-size:0.95rem; margin-bottom:24px; }

/* ── recherche ── */
.stTextInput input {
    background:#FFFFFF !important;
    border:2px solid #CBD5E1 !important;
    border-radius:12px !important;
    color:#0B1F4B !important;
    font-size:0.95rem !important;
    padding:12px 16px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
.stTextInput input:focus { border-color:#2563EB !important; box-shadow:0 0 0 3px rgba(37,99,235,0.12) !important; }
.stTextInput label { color:#334155 !important; font-weight:600 !important; font-size:0.88rem !important; }

/* ── filtres ── */
.filter-box {
    background:#FFFFFF;
    border:1px solid #E2E8F0;
    border-radius:14px;
    padding:16px 20px 8px 20px;
    margin-bottom:20px;
    box-shadow:0 1px 4px rgba(0,0,0,0.05);
}
.filter-label { color:#334155 !important; font-weight:600 !important; font-size:0.85rem !important; margin-bottom:12px; }
.stSelectbox label { color:#334155 !important; font-weight:500 !important; font-size:0.82rem !important; }
.stSelectbox > div > div {
    background:#FFFFFF !important;
    border:1.5px solid #CBD5E1 !important;
    border-radius:10px !important;
    color:#0B1F4B !important;
}

/* ── boutons ── */
.stButton > button {
    background:#FFFFFF !important; color:#334155 !important;
    border:1.5px solid #CBD5E1 !important; border-radius:10px !important;
    font-weight:500 !important; font-size:0.85rem !important;
    padding:8px 16px !important; transition:all 0.18s !important;
}
.stButton > button:hover { background:#0B1F4B !important; color:#FFFFFF !important; border-color:#0B1F4B !important; }

/* ── badge compteur ── */
.badge {
    display:inline-block;
    background:#EFF6FF; color:#1D4ED8;
    border:1px solid #BFDBFE;
    border-radius:20px; padding:5px 14px;
    font-size:0.83rem; font-weight:600;
}

/* ── cartes ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background:#FFFFFF !important;
    border:1px solid #E2E8F0 !important;
    border-radius:16px !important;
    box-shadow:0 2px 8px rgba(11,31,75,0.07) !important;
    transition:box-shadow 0.2s, transform 0.2s !important;
    overflow:hidden !important;
    padding:4px !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow:0 8px 24px rgba(11,31,75,0.13) !important;
    transform:translateY(-2px) !important;
}

/* ── subheader carte ── */
[data-testid="stVerticalBlockBorderWrapper"] h3 {
    font-family:'Sora',sans-serif !important;
    font-size:1rem !important; color:#0B1F4B !important;
    font-weight:700 !important; margin-bottom:2px !important;
}

/* ── texte carte ── */
[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p {
    color:#334155 !important;
    font-size:0.87rem !important;
    line-height:1.55 !important;
    margin:2px 0 !important;
}
[data-testid="stVerticalBlockBorderWrapper"] strong { color:#0B1F4B !important; font-weight:600 !important; }

/* ── codes / badges inline ── */
code {
    background:#EFF6FF !important;
    color:#1D4ED8 !important;
    border-radius:6px !important;
    font-size:0.8rem !important;
    padding:2px 8px !important;
    font-family:'Inter',monospace !important;
    font-weight:600 !important;
}

/* ── tarif badge ── */
.tarif-badge {
    display:inline-block;
    background:#F0FDF4; color:#166534;
    border:1px solid #BBF7D0;
    border-radius:8px; padding:3px 10px;
    font-size:0.82rem; font-weight:600;
}

/* ── bouton fiche PDF ── */
[data-testid="stVerticalBlockBorderWrapper"] .stLinkButton a {
    background:#0B1F4B !important; color:#FFFFFF !important;
    border:none !important; border-radius:10px !important;
    font-size:0.82rem !important; font-weight:600 !important;
    padding:7px 14px !important;
    transition:background 0.18s, transform 0.18s !important;
}
[data-testid="stVerticalBlockBorderWrapper"] .stLinkButton a:hover {
    background:#1D4ED8 !important;
    transform:translateY(-1px) !important;
}

/* ── expander ── */
.streamlit-expanderHeader {
    color:#334155 !important;
    font-size:0.83rem !important; font-weight:500 !important;
    background:#F8FAFC !important;
    border-radius:8px !important;
}
.streamlit-expanderContent p { color:#475569 !important; font-size:0.85rem !important; }

/* ── divider ── */
hr { border-color:#E2E8F0 !important; margin:8px 0 !important; }

/* ── caption ── */
.stCaption p { color:#94A3B8 !important; font-size:0.75rem !important; }

/* ── image placeholder ── */
[data-testid="stVerticalBlockBorderWrapper"] .stAlert {
    border-radius:10px !important; font-size:0.78rem !important;
}

/* ── section title ── */
.section-title {
    font-family:'Sora',sans-serif;
    font-size:0.72rem; font-weight:700;
    color:#94A3B8; text-transform:uppercase;
    letter-spacing:1px; margin:10px 0 4px 0;
}
</style>
""", unsafe_allow_html=True)

# ── DONNÉES ─────────────────────────────────────────────────────────────────
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

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📂 Démarche à savoir")
    st.markdown("Téléchargez les documents officiels.")
    st.divider()
    docs = [
        ("📋 Fiche de préconisation",  "1aEwrr1jAEMQE1pEiOUVs3ShwIXTKYDJ8"),
        ("📝 Évaluation des besoins",  "1OXc5N-rPpOAzI3r1F8Ov887mn_k75qoD"),
        ("🪑 VPH par catégorie",        "1_vMX4OU5tqm5OU_YtNyUel2SatFQ_VyJ"),
        ("👨‍⚕️ Qui peut prescrire ?",    "1ZRKYZhsRx_5SiUNOAMhoRC8EtesPx9ja"),
    ]
    for label, fid in docs:
        url = f"https://drive.google.com/uc?export=download&id={fid}"
        st.markdown(f'''
        <a href="{url}" target="_blank" style="
            display:block; width:100%; box-sizing:border-box;
            background:#FFFFFF; color:#0B1F4B !important;
            border-radius:10px; padding:10px 14px;
            font-size:0.88rem; font-weight:600;
            text-decoration:none; margin-bottom:8px;
            box-shadow:0 2px 8px rgba(29,78,216,0.35);
        ">{label}</a>
        ''', unsafe_allow_html=True)
    st.divider()
    st.caption("🔄 Données actualisées toutes les 60 s")

# ── MAIN ─────────────────────────────────────────────────────────────────────
st.title("🦽 Assistant Réforme VPH 2026")
st.markdown('<p class="subtitle">Consultez les fauteuils roulants, codes LPPR et conditions de prescription de la nomenclature 2026.</p>', unsafe_allow_html=True)

if df_raw is None:
    st.error("Impossible de charger les données.")
    st.stop()

df = df_raw.copy()

# Recherche
recherche = st.text_input("🔍 Rechercher un modèle, fabricant, code LPPR…", "").strip()

# Filtres
st.markdown('<div class="filter-box">', unsafe_allow_html=True)
st.markdown('<p class="filter-label">🎛️ Filtres</p>', unsafe_allow_html=True)

def opts(col):
    if col in df_raw.columns:
        vals = sorted([v for v in df_raw[col].dropna().astype(str).unique()
                       if v.lower() not in ("non spécifié","nan","code inconnu","")])
        return ["Tous"] + vals
    return ["Tous"]

c1,c2,c3,c4,c5 = st.columns(5)
with c1: f_cat  = st.selectbox("Catégorie",  opts("CATEGORIE"))
with c2: f_fab  = st.selectbox("Fabricant",  opts("FABRICANT"))
with c3: f_ref  = st.selectbox("Code Réf.",  opts("CODE_REF"))
with c4: f_cls  = st.selectbox("Classe",     opts("CLASSE"))
with c5: f_stype= st.selectbox("Sous-type",  opts("SOUS_TYPE"))
st.markdown('</div>', unsafe_allow_html=True)

# Appliquer filtres
if recherche:
    mask = df.astype(str).apply(lambda x: x.str.contains(recherche, case=False, na=False)).any(axis=1)
    df = df[mask]
for col, val in [("CATEGORIE",f_cat),("FABRICANT",f_fab),("CODE_REF",f_ref),("CLASSE",f_cls),("SOUS_TYPE",f_stype)]:
    if val != "Tous" and col in df.columns:
        df = df[df[col].astype(str)==val]

# Reset + compteur
r_col, b_col = st.columns([5,1])
with r_col:
    n = len(df)
    st.markdown(f'<span class="badge">💡 {n} modèle{"s" if n>1 else ""} trouvé{"s" if n>1 else ""}</span>', unsafe_allow_html=True)
with b_col:
    if st.button("🔄 Réinitialiser"):
        st.rerun()

st.markdown("")

# ── GRILLE ───────────────────────────────────────────────────────────────────
def clean(val, *bad):
    s = str(val).strip()
    bads = {"nan","none","non spécifié","non renseigné","code inconnu",""} | {b.lower() for b in bad}
    return None if s.lower() in bads else s

if df.empty:
    st.warning("Aucun résultat. Modifiez les filtres ou la recherche.")
else:
    left, right = st.columns(2)
    cols = [left, right]
    for idx, (_, row) in enumerate(df.iterrows()):
        with cols[idx % 2]:
            with st.container(border=True):

                fabricant = str(row.get("FABRICANT","")).strip()
                modele    = str(row.get("MODELE","")).strip()
                st.subheader(f"{fabricant} — {modele}")

                img_col, info_col = st.columns([1, 1.4])

                with img_col:
                    photo = clean(row.get("LIEN_PHOTO",""))
                    if photo and photo.lower().startswith("http"):
                        if "drive.google.com/file/d/" in photo:
                            fid = photo.split("/d/")[1].split("/")[0]
                            photo = f"https://drive.google.com/uc?export=view&id={fid}"
                        st.image(photo, use_container_width=True)
                    else:
                        st.caption("📷 Image non disponible")

                with info_col:
                    # ── Identification ──
                    st.markdown('<p class="section-title">Identification</p>', unsafe_allow_html=True)
                    for lbl, key in [("Catégorie","CATEGORIE"),("Sous-type","SOUS_TYPE"),("Classe","CLASSE"),("Usage","USAGE")]:
                        v = clean(row.get(key,""))
                        if v: st.markdown(f"**{lbl} :** {v}")

                    # ── Codes & Tarification — TOUJOURS affichés ──
                    st.divider()
                    st.markdown('<p class="section-title">Codes & Tarification</p>', unsafe_allow_html=True)

                    code_ref = str(row.get("CODE_REF","")).strip()
                    if code_ref and code_ref.lower() not in ("nan",""):
                        st.markdown(f"**CODE REF :** `{code_ref}`")

                    lppr_am = str(row.get("CODE_LPPR_ASSURANCE_MALADIE","")).strip()
                    if lppr_am and lppr_am.lower() not in ("nan",""):
                        st.markdown(f"**CODE LPPR Assurance Maladie :** `{lppr_am}`")

                    lppr_ind = str(row.get("CODE_LPPR_INDIVIDUEL_FOURNISSEUR","")).strip()
                    if lppr_ind and lppr_ind.lower() not in ("nan",""):
                        st.markdown(f"**CODE LPPR Individuel Fournisseur :** `{lppr_ind}`")

                    tarif = clean(row.get("TARIF_PRIS_EN_CHARGE",""))
                    if tarif:
                        st.markdown(f'<span class="tarif-badge">💶 {tarif}</span>', unsafe_allow_html=True)

                    # ── Technique ──
                    chassis = clean(row.get("CHASSIS",""))
                    poids   = clean(row.get("POIDS",""))
                    if chassis or poids:
                        st.divider()
                        st.markdown('<p class="section-title">Caractéristiques</p>', unsafe_allow_html=True)
                        if chassis: st.markdown(f"**Châssis :** {chassis}")
                        if poids:   st.markdown(f"**⚖️ Poids :** {poids}")

                    # ── Prescription — TOUJOURS affiché ──
                    st.divider()
                    st.markdown('<p class="section-title">Prescription</p>', unsafe_allow_html=True)

                    prescripteur = clean(row.get("PRESCRIPTEUR",""))
                    if prescripteur:
                        st.markdown(f"**👨‍⚕️ Prescripteur :** {prescripteur}")

                    libelle = str(row.get("LIBELLE_PRESCRIPTION","")).strip()
                    if libelle and libelle.lower() not in ("nan","non spécifié","code inconnu",""):
                        with st.expander("📝 Libellé de prescription"):
                            st.write(libelle)

                    descripteurs = clean(row.get("DESCRIPEURS",""))
                    if descripteurs:
                        with st.expander("🏷️ Descripteurs"):
                            st.write(descripteurs)

                    # ── Fiche technique ──
                    pdf = str(row.get("FICHE_TECHNIQUE","")).strip()
                    if pdf and pdf.lower().startswith("http"):
                        st.link_button("📄 Fiche technique (PDF)", pdf)
                    else:
                        st.caption("⚠️ Aucune fiche technique disponible")
