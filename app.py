import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ─────────────────────────────────────────────

# CONFIGURATION

# ─────────────────────────────────────────────

st.set_page_config(
page_title=“Expert VPH 2026”,
layout=“wide”,
page_icon=“🦽”,
)

SHEET_URL = (
“https://docs.google.com/spreadsheets/d/”
“1CQv9DlVzslPhlKzY-6b6XFSLDAdm_ARS1MFXKfwgjGM/export?format=csv”
)

# Colonnes attendues après normalisation (UPPER + strip)

COL_FABRICANT = “FABRICANT”
COL_MODELE = “MODELE”
COL_CATEGORIE = “CATEGORIE”
COL_PHOTO = “LIEN PHOTO”
COL_PDF = “FICHE TECHNIQUE”
COL_REF = “CODE_REF”
COL_LPPR = “CODE_LPPR”
COL_CHASSIS = “CHASSIS”
COL_LIBELLE = “LIBELLE_PRESCRIPTION”

# ─────────────────────────────────────────────

# CHARGEMENT DES DONNÉES

# ─────────────────────────────────────────────

@st.cache_data(ttl=300) # 5 min — évite les rechargements trop fréquents
def load_data() -> pd.DataFrame | None:
try:
df = pd.read_csv(SHEET_URL, dtype=str) # tout en str dès le départ
df.columns = [str(c).strip().upper() for c in df.columns]
df = df.fillna(””) # évite les NaN dans les .get()
return df
except Exception as e:
st.error(f”❌ Erreur de lecture du fichier : {e}”)
return None

def safe_get(row: pd.Series, col: str, default: str = “-”) -> str:
“”“Lecture sécurisée d’une cellule avec valeur par défaut.”””
val = row.get(col, default)
return str(val).strip() if val and str(val).strip() not in (””, “nan”) else default

def is_url(value: str) -> bool:
return str(value).lower().startswith(“http”)

# ─────────────────────────────────────────────

# COMPOSANTS D’AFFICHAGE

# ─────────────────────────────────────────────

def render_pdf_button(pdf_link: str) -> None:
“”“Bouton PDF isolé dans un composant HTML pour éviter le rechargement de page.”””
if is_url(pdf_link):
html = f”””
<div style="margin-top:6px;">
<a href="{pdf_link}" target="_blank" rel="noopener noreferrer"
style="text-decoration:none; background:#0288d1; color:#fff;
padding:8px 16px; border-radius:6px; font-family:sans-serif;
font-weight:bold; display:inline-block; font-size:13px;
box-shadow:0 2px 6px rgba(0,0,0,.25);">
📄 Fiche technique (PDF)
</a>
</div>
“””
components.html(html, height=55) # hauteur suffisante pour ne pas rogner
else:
st.caption(“⚠️ Aucune fiche PDF disponible”)

def render_card(row: pd.Series) -> None:
“”“Affiche une carte produit complète.”””
fabricant = safe_get(row, COL_FABRICANT, “Fabricant inconnu”)
modele = safe_get(row, COL_MODELE, “Modèle inconnu”)
categorie = safe_get(row, COL_CATEGORIE)
photo = safe_get(row, COL_PHOTO, “”)
pdf_link = safe_get(row, COL_PDF, “”)
ref = safe_get(row, COL_REF)
lppr = safe_get(row, COL_LPPR)
chassis = safe_get(row, COL_CHASSIS)
libelle = safe_get(row, COL_LIBELLE, “”)

```
with st.container(border=True):
    st.subheader(f"{fabricant} — {modele}")

    col_img, col_info = st.columns([1, 1.4])

    with col_img:
        if is_url(photo):
            st.image(photo, use_container_width=True)
        else:
            st.info("📷 Image non disponible")

    with col_info:
        st.markdown(f"**Catégorie :** {categorie}")
        render_pdf_button(pdf_link)

        st.markdown("---")

        st.markdown(f"**Référence :** `{ref}`")
        st.markdown(f"**Code LPPR :** `{lppr}`")
        st.markdown(f"**Châssis :** {chassis}")

        if libelle and libelle not in ("-", "Non spécifié", "non spécifié"):
            with st.expander("📝 Libellé de prescription"):
                st.write(libelle)
```

# ─────────────────────────────────────────────

# INTERFACE PRINCIPALE

# ─────────────────────────────────────────────

st.title(“🦽 Assistant Réforme VPH 2026”)
st.caption(“Données issues de la base nationale — mise à jour automatique toutes les 5 min.”)

df_raw = load_data()

if df_raw is None:
st.stop() # Arrêt propre si le chargement a échoué

# ── Filtres ────────────────────────────────

with st.expander(“🔎 Filtres de recherche”, expanded=True):
col_search, col_cat, col_cols = st.columns([2, 1.5, 1])

```
with col_search:
    recherche = st.text_input(
        "Rechercher un modèle",
        placeholder="Ex: Action, TDX, Kuschall…",
    ).strip()

with col_cat:
    categories = sorted(df_raw[COL_CATEGORIE].dropna().unique().tolist()) \
        if COL_CATEGORIE in df_raw.columns else []
    cat_selectionnee = st.selectbox(
        "Filtrer par catégorie",
        options=["Toutes"] + categories,
    )

with col_cols:
    nb_colonnes = st.selectbox("Colonnes d'affichage", options=[1, 2, 3], index=1)
```

# ── Application des filtres ────────────────

df = df_raw.copy()

if recherche:
mask = df.astype(str).apply(
lambda x: x.str.contains(recherche, case=False, na=False)
).any(axis=1)
df = df[mask]

if cat_selectionnee != “Toutes” and COL_CATEGORIE in df.columns:
df = df[df[COL_CATEGORIE] == cat_selectionnee]

# ── Résultats ──────────────────────────────

n = len(df)
if n == 0:
st.warning(“🔍 Aucun modèle ne correspond à votre recherche.”)
st.stop()

st.markdown(f”💡 **{n} modèle{‘s’ if n > 1 else ‘’}** trouvé{‘s’ if n > 1 else ‘’}.”)

cols = st.columns(nb_colonnes)
for idx, (_, row) in enumerate(df.iterrows()):
with cols[idx % nb_colonnes]:
render_card(row)
