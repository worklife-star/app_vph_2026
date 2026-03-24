# Nettoyage des noms de colonnes pour éviter les erreurs d'espaces ou de majuscules
        df_f.columns = [c.strip().upper() for c in df_f.columns]

        # Affichage
        cols = st.columns(2)
        for idx, (_, row) in enumerate(df_f.iterrows()):
            cat_color = get_cat_color(row.get('CATEGORIE', ''))
            with cols[idx % 2]:
                st.markdown(f"""
                    <div style="border-left: 8px solid {cat_color}; padding: 15px; border-radius: 10px; background-color: #ffffff; border-right: 1px solid #eee; border-top: 1px solid #eee; border-bottom: 1px solid #eee; margin-bottom: 20px;">
                        <h3 style="margin-top:0;">{row.get('FABRICANT', '')} - {row.get('MODELE', '')}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.container():
                    c1, c2 = st.columns([1, 1.5])
                    with c1:
                        img = row.get('LIEN PHOTO', '')
                        if str(img).startswith('http'):
                            st.image(img, use_container_width=True)
                        else:
                            st.info("📷 Image non dispo")
                        
                        # --- BLOC FICHE TECHNIQUE CORRIGÉ ---
                        ft_link = row.get('FICHE TECHNIQUE', '')
                        if ft_link and str(ft_link).startswith('http'):
                            st.link_button("📄 FICHE TECHNIQUE", str(ft_link), use_container_width=True, type="primary")
                        else:
                            st.caption("🚫 Pas de fiche technique")

                    with c2:
                        st.markdown(f"**Réf :** `{row.get('CODE_REF', 'N/A')}`")
                        st.markdown(f"**LPPR :** `{row.get('CODE_LPPR', 'N/A')}`")
                        st.markdown(f"**Catégorie :** <span style='color:{cat_color}; font-weight:bold;'>{row.get('CATEGORIE', 'N/A')}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Châssis :** {row.get('CHASSIS', '-')}")
                        st.markdown(f"**Dossier :** {row.get('DOSSIER', '-')}")
