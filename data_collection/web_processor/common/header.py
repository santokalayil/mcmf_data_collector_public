from PIL import Image
import streamlit as st

from . import INFO
from ...paths import COMPANY_LOGO_ICO_PATH, COMPANY_LOGO_FULL_PATH


COMPANY_LOGO = str(COMPANY_LOGO_FULL_PATH.as_uri()) # "file://corp.ezetap.com/uploads/settings/logo2.png"
# COMPANY_LOGO = "assets/logo.jpg"
# COMPANY_LOGO = "https://corp.ezetap.com/uploads/settings/logo2.png"

# st.write(COMPANY_LOGO)



# @st.cache
def add_logo():  # background-image: url({{ COMPANY_LOGO }});
    style_text = """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url({{ COMPANY_LOGO }});
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
        </style>
        """
    
    st.markdown(style_text.replace("{{ COMPANY_LOGO }}", COMPANY_LOGO), unsafe_allow_html=True)


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

# @st.cache
def draw():
    st.set_page_config(page_title=INFO["page_title"], page_icon=get_favicon(), layout=INFO["layout"])
    hide_streamlit_default_menu()
    add_logo()
    message_holder = st.sidebar.empty()
    return message_holder
