from PIL import Image
import streamlit as st

from . import INFO
from ...paths import COMPANY_LOGO_ICO_PATH  #, COMPANY_LOGO_FULL_PATH


# COMPANY_LOGO = str(COMPANY_LOGO_FULL_PATH.as_uri()) # "file://corp.ezetap.com/uploads/settings/logo2.png"
# COMPANY_LOGO = "assets/logo.jpg"
# COMPANY_LOGO = "https://raw.githubusercontent.com/santokalayil/mcmf_data_collector_public/main/assets/logo.PNG"
COMPANY_LOGO = "https://raw.githubusercontent.com/santokalayil/mcmf_data_collector_public/main/assets/logo.PNG"

# st.write(COMPANY_LOGO)



# @st.cache
def add_logo(width:str="180px", height:str="220px"):  # background-image: url({{ COMPANY_LOGO }});
    style_text = """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url({{ COMPANY_LOGO }});
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
                background-size: {{ width }}, {{ height }};
            }
        </style>
        """
                # height: 100px;
                # width: 100px;
    filled_style_text = style_text\
        .replace("{{ COMPANY_LOGO }}", COMPANY_LOGO)\
        .replace("{{ width }}", width).replace("{{ height }}", height)
    st.markdown(filled_style_text, unsafe_allow_html=True)


# @st.cache
def get_favicon():
    ico_path = str(COMPANY_LOGO_ICO_PATH)
    return Image.open(ico_path)

# @st.cache
def hide_streamlit_default_menu():
    st.markdown(""" <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)

def remove_extra_padding():
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

# @st.cache
def draw(sibebar_collapsed=True):
    st.set_page_config(
        page_title=INFO["page_title"], 
        page_icon=get_favicon(), 
        layout=INFO["layout"], 
        initial_sidebar_state="collapsed" if sibebar_collapsed is True else "expanded"
    )
    remove_extra_padding()
    hide_streamlit_default_menu()
    add_logo()
    message_holder = st.sidebar.empty()
    return message_holder
