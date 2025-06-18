import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
from utils.database_connection import get_sharepoint_db
import streamlit_shadcn_ui as ui

db_client = get_sharepoint_db()


def get_sharepoint_overview():
    col_1 = st.columns([1])[0]

    with col_1:
        content_tabs = sac.tabs([
            sac.TabsItem('SharePoint Projekter', tag='SharePoint Projekter', icon='bi bi-card-list'),
            sac.TabsItem('Sharepoint Liste info', tag='Sharepoint Liste info')
        ], color='dark', size='md', position='top', align='start', use_container_width=True)

    try:
        if 'sharepoint_data' not in st.session_state:
            results = []
            with st.spinner('Loading SharePoint data...'):
                query = """
                SELECT "Afdeling/delområde",
                       "Fase",
                       "Forvaltning",
                       "Program eller konkret indsats",
                       "Projektejer",
                       "Spor",
                       "Title",
                       "Uddybning",
                       "Status",
                       "Status - uddybning",
                       "Projektleder"
                FROM sharepoint_items_test_1
                """
                result = db_client.execute_sql(query)
                columns = [
                    "Afdeling/delområde", "Fase", "Forvaltning",
                    "Program eller konkret indsats", "Projektejer", "Spor", "Title",
                    "Uddybning", "Status", "Status - uddybning", "Projektleder"
                ]
                if result is not None:
                    results.append(pd.DataFrame(result, columns=columns))
                else:
                    st.error("Failed to fetch data from the Postgres DB.")
                    return

            if results:
                st.success("Data fetched successfully from DB.")
                st.session_state.sharepoint_data = pd.concat(results, ignore_index=True)
            else:
                st.error("No data to display.")
                return

        data = st.session_state.sharepoint_data

        if content_tabs == 'SharePoint Projekter':
            project_titles = data["Title"].dropna().unique()
            selected_project = st.selectbox('Vælg Sharepoint projekt', project_titles, help='Vælg projekt for at se detaljer')

            project_details = data[data["Title"] == selected_project].iloc[0]

            st.info(f"**Afdeling/delområde:** {project_details['Afdeling/delområde']}")

            fase = project_details["Fase"] if pd.notna(project_details["Fase"]) and project_details["Fase"] else "Ingen fase"
            projektejer = project_details["Projektejer"] if pd.notna(project_details["Projektejer"]) and project_details["Projektejer"] else "Ingen projektejere"
            forvaltning = project_details["Forvaltning"] if pd.notna(project_details["Forvaltning"]) and project_details["Forvaltning"] else "Ingen forvaltning"
            projektleder = project_details["Projektleder"] if pd.notna(project_details["Projektleder"]) and project_details["Projektleder"] else "Ingen projektleder"

            col1, col2 = st.columns(2)
            with col1:
                ui.metric_card(
                    title="Fase",
                    content=str(fase)[:50],
                    description="Fase for projekt"
                )
                ui.metric_card(
                    title="Projektejer",
                    content=str(projektejer)[:50],
                    description="Projektejer for projekt"
                )
            with col2:
                ui.metric_card(
                    title="Forvaltning",
                    content=str(forvaltning)[:50],
                    description="Forvaltning for projekt"
                )
                ui.metric_card(
                    title="Projektleder",
                    content=str(projektleder)[:50],
                    description="Projektleder for projekt"
                )

            uddybning = project_details["Uddybning"] if pd.notna(project_details["Uddybning"]) and project_details["Uddybning"] else "Ingen uddybning"

            st.markdown("### Uddybning")
            st.info(str(uddybning))

            status = project_details["Status"] if pd.notna(project_details["Status"]) and project_details["Status"] else "Ingen status"
            status_uddybning = project_details["Status - uddybning"] if pd.notna(project_details["Status - uddybning"]) and project_details["Status - uddybning"] else "Ingen status uddybning"

            st.markdown("### Status")
            st.success(f"{status}: {status_uddybning}")

            st.markdown("### Program eller konkret indsats")
            st.write(str(project_details["Program eller konkret indsats"]))

            spor = project_details["Spor"] if pd.notna(project_details["Spor"]) and project_details["Spor"] else "Ingen spor"

            st.markdown("### Spor")
            st.write(str(spor))

    except Exception as e:
        st.error(f'An error occurred: {e}')
    finally:
        db_client.close_connection()
