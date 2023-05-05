import re
import streamlit as st

from .common import footer, header
from ..config import DB_COLUMNS_INFO

from ..data_processor import load_regionwise_parishes_data
from ..gcp_processor.sheets import add_record
from ..paths import ASSETS_DIR
from PIL import Image

LOGO_IMAGE = Image.open(str(ASSETS_DIR / "logo.PNG"))


pages = st.source_util.get_pages('main.py')
new_page_names = {
    'main': "Home Page",
    'dummy': 'Form Page',
    'ploting_demo': 'Action Page',
}

for key, page in pages.items():
    if page['page_name'] in new_page_names:
        page['page_name'] = new_page_names[page['page_name']]


PARISHES = load_regionwise_parishes_data()

def render():
    global LOGO_IMAGE
    header.draw()
    
    with st.container():


        logo_col, title_col = st.columns((4, 11))
        logo_col.image(LOGO_IMAGE, use_column_width="always")
        text = "Bhavana Jyothis" # rgb(255, 0, 154)
        title_mkdwn = f'<p style="color:red; font-size: 30px; font-weight: 900;padding: 0px; margin: 0px; text-align: left;">{text}</p>'
        title_col.markdown(title_mkdwn, unsafe_allow_html=True)

        text = "Commission for Family and Women" # rgb(255, 0, 154)
        title_mkdwn = f'<p style="color:blue; font-size: 24px; font-weight: bold;padding: 0px; margin: 0px; text-align: left;">{text}</p>'
        title_col.markdown(title_mkdwn, unsafe_allow_html=True)


        title_mkdwn = '<p style="color:rgb(255, 0, 154); font-size: 22px; font-weight: normal; padding: 0px; margin: 0px; text-align: left;">Diocese of Puttur</p>'
        title_col.markdown(title_mkdwn, unsafe_allow_html=True)
        
        text = "The Syro-Malankara Catholic Church".upper()
        title_mkdwn = f'<p style="color:black; font-size: 20px; font-weight: normal; padding: 0px; margin: 0px; text-align: left;">{text}</p>'
        title_col.markdown(title_mkdwn, unsafe_allow_html=True)

        st.markdown("---")

        title_mkdwn = '<p style="color:rgb(114, 0, 71); font-size: 34px; font-weight: 900; padding: 0px; margin: 0px;">Data Collection Drive <span style="color:rgb(255, 13, 71);">2k23</span></p>'
        st.markdown(title_mkdwn, unsafe_allow_html=True)
        # title_col.title(":violet[MCMF] Data Collection")
        # title_col.header(":red[DIOCESE OF PUTTUR]")
        # title_col.subheader("The Syro-Malankara Catholic Church")
        
        st.caption("A Venture to collect, analyse and understand about Mathruvedi Members")
        # st.markdown("---")
        with st.expander("See the instructions before filling the form below "):
            st.write("""
                The chart above shows some numbers I picked for you.
                I rolled actual dice for these, so they're *guaranteed* to
                be random.
            """)


    # st.markdown("---")

    # st.write("Enter the following information:")

    # message_holder = st.empty()

    error_messages = []

    VALID_FORM_DATA = True  # False is to be default
    EXTRA_FIELDS_AFTER_VALIDATION = {}
    with st.form(key="form", clear_on_submit=False):
        for col, params in DB_COLUMNS_INFO.items():
            label = col if params['question'] == "" else params['question']

            if col == "region":
                selected_region =st.selectbox(label, options=PARISHES.keys(), key=col)
            elif col == "parish":
                st.selectbox(label, options=PARISHES[selected_region])


            elif params["type"] == 'text':
                st.text_input(label, key=col)
            elif params['type'] == 'date':
                st.date_input(label, key=col)
            elif params['type'] == "email":
                possible_email_text = st.text_input(label, key=col)
                if possible_email_text.strip():
                    email_list = re.findall(r"\w+[_\.\+]*\w+@[a-zA-Z]{3,10}[.][a-z]+[.]*[a-z]*[ ,]*", possible_email_text)
                    if email_list:
                        EXTRA_FIELDS_AFTER_VALIDATION[col] = email_list[0]
                    else:
                        error_messages.append("email is invalid")
            
        data = {col:st.session_state[col] for col in DB_COLUMNS_INFO.keys() if col in st.session_state.keys()}
        st.json(data, expanded=False)

        # VALIDATION SECTION
        data = {col: EXTRA_FIELDS_AFTER_VALIDATION[col] if col in EXTRA_FIELDS_AFTER_VALIDATION else value for col, value in data.items() }

        NULL_VALIDATION_ENABLED = True
        if NULL_VALIDATION_ENABLED is True:
            empty_fields = []
            for key, params in DB_COLUMNS_INFO.items():
                if key in data:
                    if params['can_be_null'] is False:
                        if not data[key]:
                            empty_fields.append(key)
            if empty_fields:
                error_messages.append(f"The following fields cannot be empty: '{', '.join(empty_fields)}'")

        
                

                

        st.caption("After adding extra fields after validation")
        st.json(data, expanded=False)

        if st.form_submit_button(
            label="Submit", 
            help=None, 
            on_click=None, 
            args=None, 
            kwargs=None, 
            type="secondary", 
            disabled=not VALID_FORM_DATA, 
            use_container_width=True
        ) is True:
            if error_messages:
                with st.container():
                    for err_msg in error_messages:
                        st.error(err_msg)
            else:
                serialized_data = serialize_data(data)
                add_record(columns_data=serialized_data)
                st.success("Data successfully submitted")
        # else:
        #     st.error("Data submission unsuccessful")





    footer.draw()


def serialize_data(data):
    for col, params in DB_COLUMNS_INFO.items():
        if col in data:
            if params['type'] == 'date':
                data[col] = data[col].strftime("%b %d %Y")
    return data