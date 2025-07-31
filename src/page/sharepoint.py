import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
from utils.database_connection import get_sharepoint_db
from utils.util import filter_forvaltning_options, get_fase_icon, starts_with_letter, map_projekt_fase, map_forvaltning_forkortelse, filter_teknologi_options

db_client = get_sharepoint_db()


def get_sharepoint_overview():

    col_1 = st.columns([1])[0]

    with col_1:
        content_tabs = sac.tabs([
            sac.TabsItem('Projektoversigt', tag='Teknologi- og Digitaliseringsprojekter i Randers Kommune', icon='bi bi-card-list'),
        ], color='dark', size='md', position='top', align='start', use_container_width=True)

    try:
        if 'sharepoint_data' not in st.session_state:
            results = []
            with st.spinner('Loading SharePoint data...'):
                query = """
                SELECT "Forvaltning",
                       "Title",
                       "Uddybning",
                       "Teknologi",
                       "Projektleder_Name",
                       "Projektleder_Email",
                       "Projektejer_Name",
                       "Projektejer_Email",
                       "Fase",
                       "Program eller konkret indsats"
                FROM sharepoint_handleplan_items
                """
                result = db_client.execute_sql(query)
                columns = [
                    "Forvaltning", "Title",
                    "Uddybning", "Teknologi",
                    "Projektleder_Name", "Projektleder_Email",
                    "Projektejer_Name", "Projektejer_Email",
                    "Fase", "Program eller konkret indsats"
                ]
                if result is not None:
                    results.append(pd.DataFrame(result, columns=columns))
                else:
                    st.error("Failed to fetch data from the Postgres DB.")
                    return

            if results:
                st.session_state.sharepoint_data = pd.concat(results, ignore_index=True)
            else:
                st.error("No data to display.")
                return

        data = st.session_state.sharepoint_data

        if content_tabs == 'Projektoversigt':
            with st.sidebar:
                st.markdown("### 🔎 Filtrer projekter")

                search_query = st.text_input("Søg Projekt", value="", placeholder="Søg", label_visibility="collapsed")

                forvaltning_options = filter_forvaltning_options(sorted(data["Forvaltning"].dropna().unique().tolist()))
                forvaltning_filter = st.selectbox(
                    "Vælg Forvaltning",
                    options=["Alle"] + forvaltning_options,
                )

                teknologi_options = filter_teknologi_options(sorted(data["Teknologi"].dropna().unique().tolist()))
                teknologi_filter = st.selectbox(
                    "Vælg Teknologi",
                    options=["Alle"] + teknologi_options,
                )

                data["Fase_mapped"] = data["Fase"].apply(map_projekt_fase)
                fase_options = sorted([f for f in data["Fase_mapped"].dropna().unique().tolist() if f != "Idé"])
                fase_filter = st.selectbox(
                    "Vælg Fase",
                    options=["Alle"] + fase_options,
                )

            filtered_data = data.copy()
            if search_query.strip():
                filtered_data = filtered_data[
                    filtered_data["Title"].str.contains(search_query, case=False, na=False) |
                    filtered_data["Uddybning"].str.contains(search_query, case=False, na=False)
                ]
            if forvaltning_filter != "Alle":
                filtered_data = filtered_data[filtered_data["Forvaltning"] == forvaltning_filter]
            if teknologi_filter != "Alle":
                filtered_data = filtered_data[filtered_data["Teknologi"] == teknologi_filter]
            if fase_filter != "Alle":
                filtered_data = filtered_data[filtered_data["Fase_mapped"] == fase_filter]

            filtered_data = filtered_data[filtered_data["Fase"] != "Idé"]

            filtered_data = filtered_data[
                ~filtered_data["Program eller konkret indsats"].isin([
                    "Handleplan på direktørområdet",
                    "Tværgående handleplan"
                ])
            ]

            if filtered_data.empty:
                st.warning("Ingen projekter matcher dine filtre.")
                st.stop()

            filtered_data["Title"] = filtered_data["Title"].apply(lambda x: str(x).strip())

            filtered_data = filtered_data.assign(
                starts_with_letter=filtered_data["Title"].apply(starts_with_letter)
            ).sort_values(
                by=["starts_with_letter", "Title"],
                ascending=[False, True]
            ).drop(columns=["starts_with_letter"])

            st.markdown(
                f"<span style='background:#e0e0e0; border-radius:8px; padding:4px 12px; font-size:0.95rem; margin-left:8px;'>🔎 {len(filtered_data)} projekter fundet</span>",
                unsafe_allow_html=True
            )

            for i, row in filtered_data.iterrows():
                projektleder_name = row['Projektleder_Name'] or ''
                projektleder_email = row['Projektleder_Email'] or ''
                projektejer_name = row.get('Projektejer_Name', '') or ''
                projektejer_email = row.get('Projektejer_Email', '') or ''

                if projektleder_name.strip():
                    kontakt_name = projektleder_name
                    kontakt_email = projektleder_email
                elif projektejer_name.strip():
                    kontakt_name = projektejer_name
                    kontakt_email = projektejer_email
                else:
                    kontakt_name = "Ikke angivet"
                    kontakt_email = ""

                if kontakt_email and kontakt_name != 'Ikke angivet':
                    kontakt_html = f'<a href="mailto:{kontakt_email}" title="{kontakt_email}">{kontakt_name}</a>'
                else:
                    kontakt_html = kontakt_name

                flex_content = f'<span><strong>👤</strong> {kontakt_html}</span>'
                if row["Forvaltning"]:
                    forvaltning_forkortet = map_forvaltning_forkortelse(row["Forvaltning"])
                    flex_content += f'<span style="margin-left:1rem;"><strong>🏢</strong> {forvaltning_forkortet}</span>'
                if row["Teknologi"]:
                    flex_content += f'<span><strong>⚙️</strong> {row["Teknologi"]}</span>'
                if row["Fase"]:
                    fase_icon = get_fase_icon(row["Fase"])
                    mapped_fase = map_projekt_fase(row["Fase"])
                    flex_content += f'<span><strong>{fase_icon}</strong> {mapped_fase or row["Fase"]}</span>'

                with st.expander(f"**{row['Title']}**"):
                    st.markdown(
                        f"""
                        <div style="background-color:#f8f4ed; padding:1rem; border-radius:10px; margin-bottom:1rem; border: 1px solid #9E9E9E; border-left: 5px solid #9E9E9E;">
                            <p style="margin-top:0.5rem;">{row['Uddybning'] or 'Ikke angivet'}</p>
                            <hr>
                            <div style="display:flex; justify-content:space-between;">
                                {flex_content}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    except Exception as e:
        st.error(f'An error occurred: {e}')
    finally:
        db_client.close_connection()
