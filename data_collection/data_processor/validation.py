import re
import streamlit as st
from ..config import DB_COLUMNS_INFO


def validate_session_input_data():
    data = {col:st.session_state[col] for col in DB_COLUMNS_INFO.keys() if col in st.session_state.keys()}

    error_messages = set()

    empty_fields = []
    NULL_VALIDATION_ENABLED: bool = True
    if NULL_VALIDATION_ENABLED is True:
        for key, params in DB_COLUMNS_INFO.items():
            if key in data:
                if params['can_be_null'] is False:
                    if not data[key]:
                        empty_fields.append(key)
    
    # adding empty field related errors
    if empty_fields:
        error_messages.add(f"The following fields cannot be empty: '{', '.join(empty_fields)}'")

    # invalid_email:
    field = "email"
    possible_email_text = st.session_state[field]
    if possible_email_text.strip():
        email_list = re.findall(r"\w+[_\.\+]*\w+@[a-zA-Z]{3,10}[.][a-z]+[.]*[a-z]*[ ,]*", possible_email_text)
        if email_list:
            data[field] = email_list[0]
        else:
            error_messages.add("email is invalid")
    
    # validating phone number
    phone_number_input = st.session_state['phone']
    if phone_number_input.strip():
        plus_removed = phone_number_input.strip().strip("+")
        space_removed = "".join([i for i in plus_removed.split()])  # removing spaces
        hyphe_removed = "".join([i for i in space_removed.split("-")])  # remvoing hyphens
        cleaned_text = hyphe_removed

        if not cleaned_text.isnumeric():
            error_messages.add(f"Phone number added is having non-numeric characters. ")

    data_valid = False if error_messages else True
    return data_valid, data, error_messages


