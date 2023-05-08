import re
import streamlit as st
import datetime

import pandas as pd

from .common import footer, header
from ..config import DB_COLUMNS_INFO

from ..data_processor import PARISHES, serialize_data, get_parishes_in_the_region, find_region
from ..data_processor.validation import validate_session_input_data
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


# sending_success = False
# serialization_of_data_completed = False

def render():
    global LOGO_IMAGE  #, sending_success, serialization_of_data_completed
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

        st.divider()

        title_mkdwn = '<p style="color:rgb(114, 0, 71); font-size: 34px; font-weight: 900; padding: 0px; margin: 0px;">Data Collection Drive <span style="color:rgb(255, 13, 71);">2k23</span></p>'
        st.markdown(title_mkdwn, unsafe_allow_html=True)
        
        st.caption("A Venture to collect, analyse and understand about Mathruvedi Members")
        # st.markdown("---")
        with st.expander("Instructions", expanded=False):
            st.write("""
                1. Do this
                2. Do this
            """)
            # st.markdown("<br />", unsafe_allow_html=True)
    
    st.markdown("<br />", unsafe_allow_html=True)
    
    # st.caption()

    with st.expander("Form", expanded=True):
        st.caption("Carefully input the following information")
        for col, params in DB_COLUMNS_INFO.items():
            label = col if params['question'] == "" else params['question']
            
            
            if col == "region":
                selected_region = st.selectbox(label, options=PARISHES.keys(), key=col)
            elif col == "parish":
                st.selectbox(label, options=PARISHES[selected_region] if selected_region in PARISHES.keys() else [])


            elif params["type"] == 'text':
                st.text_input(label, key=col)
            elif params['type'] == 'date':
                today = datetime.date.today()
                if col == "dob":
                    valid_adult_age = datetime.date(today.year - 18, today.month, today.day-1)
                    max_value = valid_adult_age
                    min_value = datetime.date(max_value.year-120, max_value.month, max_value.day)
                elif col == "dom":
                    selected_dob = st.session_state['dob']
                    min_value = datetime.date(selected_dob.year + 12, selected_dob.month, selected_dob.day)
                    max_value = today
                else:
                    raise Exception("Not implemented")
                
                help_text = f"""Min value: {min_value}, max_value: {max_value}"""
                st.date_input(label, key=col, value=max_value, min_value=min_value, max_value=max_value, help=help_text)
            elif params['type'] == "email":
                st.text_input(label, key=col)
            elif params['type'] == 'text-area':
                st.text_area(label, key=col)
                

        st.caption("Data to be send")
        st.json(st.session_state, expanded=False)

        

        if st.button(label="Continue",  type="secondary", use_container_width=True) is True:
            valid_data, validated_data, error_messages = validate_session_input_data()
            if  valid_data:
                # serialized_data = serialize_data(validated_data)
                # add_record(columns_data=serialized_data)
                st.success("Data validation completed! Please confirm the below information")

                view_df = pd.DataFrame([validated_data]).T.reset_index()
                view_df.index = [i+1 for i in range(view_df.shape[0])]
                view_df.columns = ["Fields", "Data"]
                st.table(view_df)

                st.warning("If any data to be edited, please go above and edit and click 'Continue' then 'Confirm & Send'")
                st.button(
                    'Confirm & Send', key="send_data_button", on_click=lambda: send_data(validated_data),
                    type="primary",
                    use_container_width=True
                )
            else:
                with st.container():
                    for err_msg in error_messages:
                        st.error(err_msg)
        
        # if serialization_of_data_completed:
        #     if serialized_data is not None:
        #         # with st.container():
        #         if st.button(label="Data is confirmed. Send", key="confirm_send"):
            
        #         if sending_success:
        #             st.success("Data successfully submitted")
        #             st.button("complete")
        #             # Delete all the items in Session state
        #             for key in st.session_state.keys():
        #                 del st.session_state[key]
                    
        #             sending_success = False




    footer.draw()



def send_data(data):
    serialized_data = serialize_data(data)
    add_record(columns_data=serialized_data)
    st.success("SENDING SUCCESS")
    st.map()



        




