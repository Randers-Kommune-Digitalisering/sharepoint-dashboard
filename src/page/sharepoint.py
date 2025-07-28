import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
from utils.database_connection import get_sharepoint_db

db_client = get_sharepoint_db()


def get_sharepoint_overview():

    col_1 = st.columns([1])[0]

    with col_1:
        content_tabs = sac.tabs([
            sac.TabsItem('SharePoint Projekter', tag='SharePoint Projekter', icon='bi bi-card-list'),
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
                       "Projektleder_Email"
                FROM sharepoint_handleplan_items
                """
                result = db_client.execute_sql(query)
                columns = [
                    "Forvaltning", "Title",
                    "Uddybning", "Teknologi",
                    "Projektleder_Name", "Projektleder_Email"
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

        if content_tabs == 'SharePoint Projekter':
            project_titles = ["Alle"] + sorted(data["Title"].dropna().unique().tolist())
            selected_title_filter = st.selectbox(
                "Søg på projekt",
                options=project_titles,
                help="Vælg et projekt for at filtrere på titel"
            )

            colf1, colf2 = st.columns(2)
            with colf1:
                forvaltning_filter = st.selectbox(
                    "Filtrer på Forvaltning",
                    options=["Alle"] + sorted(data["Forvaltning"].dropna().unique().tolist()),
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

            for i, row in filtered_data.iterrows():
                projektleder_name = row['Projektleder_Name'] or 'Ikke angivet'
                projektleder_email = row['Projektleder_Email'] or ''
                if projektleder_email and projektleder_name != 'Ikke angivet':
                    projektleder_html = f'<a href="mailto:{projektleder_email}" title="{projektleder_email}">{projektleder_name}</a>'
                else:
                    projektleder_html = projektleder_name

                st.markdown(
                    """
                    <style>
                    .responsive-card {
                        width: 100%;
                        max-width: 600px;
                        min-width: 220px;
                        margin-left: auto;
                        margin-right: auto;
                        box-sizing: border-box;
                    }
                    @media (max-width: 700px) {
                        .responsive-card {
                            max-width: 98vw;
                            padding: 0.5rem !important;
                        }
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""
                    <div class="responsive-card" style="border: 1px solid #9E9E9E; border-left: 5px solid #9E9E9E; padding: 1rem; margin-bottom: 1rem; border-radius: 5px; background-color: #f8f4ed;">
                        <h4 style="margin: 0;">{row['Title']}</h4>
                        <p style="margin: 0.5rem 0;"><strong>Uddybning af Indsats:</strong> {row['Uddybning'] or 'Ikke angivet'}</p>
                        <div style="display: flex; justify-content: space-between;">
                            <p style="margin: 0;"><strong>Projektleder:</strong> {projektleder_html}</p>
                            <p style="margin: 0;"><strong>Teknologi:</strong> {row['Teknologi'] or 'Ikke angivet'}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f'An error occurred: {e}')
    finally:
        db_client.close_connection()
