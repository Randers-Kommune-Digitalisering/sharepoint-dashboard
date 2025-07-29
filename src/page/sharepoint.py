import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
from utils.database_connection import get_sharepoint_db
from utils.util import filter_forvaltning_options, starts_with_letter

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
                       "Projektejer_Email"
                FROM sharepoint_handleplan_items
                """
                result = db_client.execute_sql(query)
                columns = [
                    "Forvaltning", "Title",
                    "Uddybning", "Teknologi",
                    "Projektleder_Name", "Projektleder_Email",
                    "Projektejer_Name", "Projektejer_Email"
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
            project_titles = ["Alle"] + sorted(data["Title"].dropna().unique().tolist())
            selected_title_filter = st.selectbox(
                "Søg på projekt",
                options=project_titles,
                help="Vælg et projekt for at filtrere på titel"
            )

            colf1, colf2 = st.columns(2)
            with colf1:
                forvaltning_options = filter_forvaltning_options(sorted(data["Forvaltning"].dropna().unique().tolist()))
                forvaltning_filter = st.selectbox(
                    "Filtrer på Forvaltning",
                    options=["Alle"] + forvaltning_options,
                    help="Vælg forvaltning for at filtrere"
                )

            with colf2:
                teknologi_filter = st.selectbox(
                    "Filtrer på Teknologi",
                    options=["Alle"] + sorted(data["Teknologi"].dropna().unique().tolist()),
                    help="Vælg teknologi for at filtrere"
                )

            filtered_data = data.copy()
            if selected_title_filter != "Alle":
                filtered_data = filtered_data[filtered_data["Title"] == selected_title_filter]
            if forvaltning_filter != "Alle":
                filtered_data = filtered_data[filtered_data["Forvaltning"] == forvaltning_filter]
            if teknologi_filter != "Alle":
                filtered_data = filtered_data[filtered_data["Teknologi"] == teknologi_filter]

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

            st.success(f"{len(filtered_data)} projekter fundet.")

            for i, row in filtered_data.iterrows():
                projektleder_name = row['Projektleder_Name'] or ''
                projektleder_email = row['Projektleder_Email'] or ''
                projektejer_name = row.get('Projektejer_Name', '') or ''
                projektejer_email = row.get('Projektejer_Email', '') or ''

                if projektleder_name.strip():
                    kontakt_label = "Projektleder"
                    kontakt_name = projektleder_name
                    kontakt_email = projektleder_email
                elif projektejer_name.strip():
                    kontakt_label = "Projektejer"
                    kontakt_name = projektejer_name
                    kontakt_email = projektejer_email
                else:
                    kontakt_label = "Projektleder"
                    kontakt_name = "Ikke angivet"
                    kontakt_email = ""

                if kontakt_email and kontakt_name != 'Ikke angivet':
                    kontakt_html = f'<a href="mailto:{kontakt_email}" title="{kontakt_email}">{kontakt_name}</a>'
                else:
                    kontakt_html = kontakt_name

                st.markdown(
                    f"""
                    <div style="background-color:#f8f4ed; padding:1rem; border-radius:10px; margin-bottom:1rem; border: 1px solid #9E9E9E; border-left: 5px solid #9E9E9E;">
                        <span style="margin: 0; font-weight: bold; font-size: 1rem;">{row['Title']}</span>
                        <p style="margin-top:0.5rem;">{row['Uddybning'] or 'Ikke angivet'}</p>
                        <hr>
                        <div style="display:flex; justify-content:space-between;">
                            <span><strong>👤 {kontakt_label}:</strong> {kontakt_html}</span>
                            <span><strong>⚙️ Teknologi:</strong> {row['Teknologi'] or 'Ikke angivet'}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f'An error occurred: {e}')
    finally:
        db_client.close_connection()
