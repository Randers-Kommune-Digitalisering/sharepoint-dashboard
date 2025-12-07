def get_custom_css():
    return """
        <span class="css-injector"></span>
        <style>
            .stMain {
                margin-top: 3.75rem;
                height: calc(100dvh - .5rem);
            }
            .stMainBlockContainer {
                padding-top: 1rem;
            }
            .stApp, .stAppHeader, .stMainBlockContainer, .stBottom > div {
                background-color: #FFFEFA;
            }
            section:has(.stMainBlockContainer) {
                scrollbar-gutter: stable;
            }

            /* Topbar custom styles */
            .stAppToolbar {
                background-color: #FCFAF4;
                border-bottom: 1px solid #e0ded3;
            }
            [data-testid="stElementContainer"]:has(.css-injector) + div[data-testid="stLayoutWrapper"] {
                display: none;
            }
            [data-testid="stElementContainer"]:has(.overlay-header-title) {
                order: 999;
                position: absolute;
                display: flex;
                top: 1.2rem;
                z-index: 9999993;
                pointer-events: none;
                font-weight: 600;
            }

            /* Sidebar custom styles */
            .stSidebar {
                z-index: 999992;
                border-right: 1px solid #e0ded3;
                background-color: #f5f3eb;
            }
            section[data-testid="stSidebar"][aria-expanded="true"] {
                min-width: 15rem;
            }
            .stSidebar .stHeading h1 {
                padding-top: 0;
            }

            /* Input and select custom styles */
            div[data-baseweb="select"] > div, div[data-baseweb="input"],
            div[data-testid="stTextInputRootElement"] > div[data-baseweb="base-input"] {
                border: 0;
                outline: 1px solid #e0ded3;
                background-color: #FFFEFA;
            }
            div[data-baseweb="select"]:has(input:focus) > div, div[data-baseweb="input"]:has(input:focus)
            {
                outline: 1px solid #b3c4a1;
            }
            
            /* Expander custom styles (project list) */
            div[data-testid="stLayoutWrapper"] > .stExpander > details {
                background-color: #b3c4a1;
                border: 0;
            }
            div[data-testid="stLayoutWrapper"] > .stExpander > details[open] {
                background-color: #FCFAF4;
                outline: 1px solid #c2d0b3;
                outline-offset: -1px;
            }
            div[data-testid="stLayoutWrapper"] > .stExpander > details[open] > summary {
                background-color: #c2d0b3;
            }
            div[data-testid="stLayoutWrapper"] > .stExpander > details > summary {
                padding: 1rem 0.8rem;
            }
            div[data-testid="stLayoutWrapper"]:hover > .stExpander > details > summary {
                background-color: #c2d0b3;
            }

            /* Custom element styles */
            .tag {
                background-color: #f5f3eb;
                border-radius: 0.5rem;
                padding: 0.8rem 1.2rem;
                font-size: 0.95rem;
                width: fit-content;
                display: inline-block;
                outline: 1px solid #e0ded3;
            }
            .projects-flex-item {
                display: inline-block;
                min-width: 20%;
            }
            .projects-flex-item > div:first-child {
                font-size: 0.8em;
                color: #555555;
                font-weight: 600;
            }
            .projects-flex-item > div:last-child {
                padding-left: 0.2rem;
                padding-right: 0.2rem;
                padding-top: 0.5rem;
            }


            @media (prefers-color-scheme: dark) {
                p {
                    color: #e8e8e8;
                }
                .stAppToolbar {
                    background-color: #27292b;
                    border-bottom: 1px solid #3d3e40;
                }
                .stApp, .stAppHeader, .stMainBlockContainer, .stBottom > div{
                    background-color: #222326;
                }
                .stSidebar {
                    border-right: 1px solid #363739;
                    background-color: #252629;
                }
                div[data-baseweb="select"] > div, div[data-baseweb="input"],
                div[data-testid="stTextInputRootElement"] > div[data-baseweb="base-input"] {
                    background-color: #4d5156;
                    outline: 1px solid #787878;
                }
                div[data-baseweb="select"]:has(input:focus) > div, div[data-baseweb="input"]:has(input:focus)
                {
                    outline: 1px solid #b3c4a1;
                }
                div[data-testid="stLayoutWrapper"] > .stExpander > details {
                    background-color: #565e4c;
                }
                div[data-testid="stLayoutWrapper"] > .stExpander > details > summary {
                    color: #f2f2f2;
                }
                div[data-testid="stLayoutWrapper"] > .stExpander > details[open] {
                    background-color: #27292b;
                    outline: 1px solid #646e58;
                }
                div[data-testid="stLayoutWrapper"] > .stExpander > details[open] > summary {
                    background-color: #646e58;
                }
                div[data-testid="stLayoutWrapper"]:hover > .stExpander > details > summary {
                    background-color: #646e58;
                }
                .tag {
                    background: #252629;
                    outline: 1px solid #3d3e40;
                }
                .projects-flex-item > div:first-child {
                    color: #878787;
                }
            }
        </style>
    """
