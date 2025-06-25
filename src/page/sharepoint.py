import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
from utils.database_connection import get_sharepoint_db
import streamlit_shadcn_ui as ui

db_client = get_sharepoint_db()


def get_sharepoint_overview():
    if 'rerun_trigger' in st.session_state and st.session_state.rerun_trigger:
        st.session_state.rerun_trigger = False
        st.rerun()

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
                FROM sharepoint_handleplan_items
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
                st.session_state.sharepoint_data = pd.concat(results, ignore_index=True)
            else:
                st.error("No data to display.")
                return

        data = st.session_state.sharepoint_data

        if content_tabs == 'SharePoint Projekter':
            if 'selected_project' not in st.session_state:
                project_titles = ["Alle"] + sorted(data["Title"].dropna().unique().tolist())
                selected_title_filter = st.selectbox(
                    "Søg på projekt",
                    options=project_titles,
                    help="Vælg et projekt for at filtrere på titel"
                )

                filtered_data = data.copy()
                if selected_title_filter != "Alle":
                    filtered_data = filtered_data[filtered_data["Title"] == selected_title_filter]

                for i, row in filtered_data.iterrows():
                    status = str(row['Status']).strip().lower() if pd.notna(row['Status']) else "ukendt"
                    color_map = {
                        'ukendt': '#9E9E9E',
                        'grøn': '#4CD450',
                        'gul': "#FDE618",
                        'rød': "#F51808"
                    }
                    color = color_map.get(status, '#9E9E9E')

                    with st.form(key=f"project_form_{i}"):
                        st.markdown(
                            f"""
                            <div style="border: 1px solid {color}; border-left: 5px solid {color}; padding: 1rem; margin-bottom: 1rem; border-radius: 5px; background-color: #f8f4ed;">
                                <h4 style="margin: 0;">{row['Title']}</h4>
                                <p style="margin: 0.5rem 0;"><strong>Uddybning af Indsats:</strong> {row['Uddybning'] or 'Ikke angivet'}</p>
                                <div style="display: flex; justify-content: space-between;">
                                    <p style="margin: 0;"><strong>Projektleder:</strong> {row['Projektleder'] or 'Ikke angivet'}</p>
                                    <p style="margin: 0;"><strong>Projektets status:</strong> {row['Status'] or 'Ikke angivet'}</p>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        submit_button = st.form_submit_button("Se flere detaljer")
                        if submit_button:
                            st.session_state['selected_project'] = row['Title']
                            st.session_state['rerun_trigger'] = True
                            st.rerun()

            else:
                selected_title = st.session_state['selected_project']
                project_details = data[data["Title"] == selected_title].iloc[0]

                if st.button("← Tilbage"):
                    st.session_state.pop("selected_project")
                    st.rerun()

                st.markdown(f"### {selected_title} ")
                st.info(f"**Afdeling/delområde:** {project_details['Afdeling/delområde']}")

                fase = project_details["Fase"] if pd.notna(project_details["Fase"]) else "Ingen fase"
                projektejer = project_details["Projektejer"] if pd.notna(project_details["Projektejer"]) else "Ingen projektejere"
                forvaltning = project_details["Forvaltning"] if pd.notna(project_details["Forvaltning"]) else "Ingen forvaltning"
                projektleder = project_details["Projektleder"] if pd.notna(project_details["Projektleder"]) else "Ingen projektleder"

                col1, col2 = st.columns(2)
                with col1:
                    ui.metric_card(title="Fase", content=str(fase), description="Fase for projekt")
                    ui.metric_card(title="Projektejer", content=str(projektejer), description="Projektejer for projekt")
                with col2:
                    ui.metric_card(title="Forvaltning", content=str(forvaltning), description="Forvaltning for projekt")
                    ui.metric_card(title="Projektleder", content=str(projektleder), description="Projektleder for projekt")

                uddybning = project_details["Uddybning"] if pd.notna(project_details["Uddybning"]) else "Ingen uddybning"
                st.markdown("### Uddybning")
                st.info(str(uddybning))

                status = project_details["Status"] if pd.notna(project_details["Status"]) else "Ingen status"
                status_uddybning = project_details["Status - uddybning"] if pd.notna(project_details["Status - uddybning"]) else "Ingen status uddybning"
                st.markdown("### Status")
                st.success(f"{status}: {status_uddybning}")

                st.markdown("### Program eller konkret indsats")
                st.write(str(project_details["Program eller konkret indsats"]))

                spor = project_details["Spor"] if pd.notna(project_details["Spor"]) else "Ingen spor"
                st.markdown("### Spor")
                st.write(str(spor))

    except Exception as e:
        st.error(f'An error occurred: {e}')
    finally:
        db_client.close_connection()
