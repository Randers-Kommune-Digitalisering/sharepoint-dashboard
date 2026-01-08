import streamlit as st
import pandas as pd
from utils.database_connection import get_sharepoint_db
from utils.util import filter_forvaltning_options, get_fase_icon, starts_with_letter, map_projekt_fase, map_forvaltning_forkortelse, filter_teknologi_options
from utils.markdown_elements import get_custom_css

db_client = get_sharepoint_db()


def get_sharepoint_overview():
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    st.markdown(
        "<div class='overlay-header-title'>Teknologi- og Digitaliseringsprojekter</div>",
        unsafe_allow_html=True
    )

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

        # if content_tabs == 'Projektoversigt':
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

            data = data.copy()
            data["Fase_mapped"] = data["Fase"].apply(map_projekt_fase)
            fase_options = sorted([f for f in data["Fase_mapped"].dropna().unique().tolist() if f != "Idé"])
            custom_fase_options = ["Alle (÷ i drift, afvist)", "Alle"] + fase_options
            # Sæt "Alle (÷ i drift)" som default
            fase_filter = st.selectbox(
                "Vælg Fase",
                options=custom_fase_options,
                index=0
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

        if fase_filter == "Alle (÷ i drift, afvist)":
            filtered_data = filtered_data[~filtered_data["Fase_mapped"].isin(["I drift", "Afvist"])]
        elif fase_filter != "Alle":
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
            f"<div class='tag' style='margin-bottom: 2rem'>🔎 <b>{len(filtered_data)}</b> projekter fundet</div>",
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

            def print_flex_item(row, content):
                return f'<div class="projects-flex-item"><div>{row}</div><div>{content}</div></div>'

            flex_content = print_flex_item("👤 Kontaktperson", kontakt_html)
            if row["Forvaltning"]:
                forvaltning_forkortet = map_forvaltning_forkortelse(row["Forvaltning"])
                flex_content += print_flex_item("🏢 Forvaltning", forvaltning_forkortet)
            if row["Teknologi"]:
                flex_content += print_flex_item("⚙️ Teknologi", row["Teknologi"])
            if row["Fase"]:
                fase_icon = get_fase_icon(row["Fase"])
                mapped_fase = map_projekt_fase(row["Fase"])
                flex_content += print_flex_item(fase_icon + " Fase", mapped_fase or row["Fase"])

            with st.expander(f"**{row['Title']}**"):
                st.markdown(
                    f"""
                    <p>{row['Uddybning'] or 'Ingen beskrivelse'}</p>
                    <hr style="margin-top: 0.5rem; margin-bottom: 1rem;">
                    <div style="display:flex; justify-content:space-between;margin-bottom: 1.5rem">
                        {flex_content}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f'An error occurred: {e}')
    finally:
        db_client.close_connection()
