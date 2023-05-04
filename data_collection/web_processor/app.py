import re
import streamlit as st

from .common import footer, header
from ..config import DB_COLUMNS_INFO

from ..gcp_processor.sheets import add_record

    

pages = st.source_util.get_pages('main.py')
new_page_names = {
    'main': "Home Page",
    'dummy': 'Form Page',
    'ploting_demo': 'Action Page',
}

for key, page in pages.items():
    if page['page_name'] in new_page_names:
        page['page_name'] = new_page_names[page['page_name']]


def render():
    header.draw()
    st.write("Enter the following information:")

    message_holder = st.sidebar.empty()

    error_messages = []

    VALID_FORM_DATA = True  # False is to be default
    EXTRA_FIELDS_AFTER_VALIDATION = {}
    with st.form(key="form", clear_on_submit=False):
        for col, params in DB_COLUMNS_INFO.items():
            label = col if params['question'] == "" else params['question']
            if params["type"] == 'text':
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
                with message_holder.container():
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