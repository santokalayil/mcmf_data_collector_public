import json
import streamlit as st
from ..paths import ASSETS_DIR

def load_info():
    info_json_path = ASSETS_DIR / "info.json"
    with open(info_json_path) as f:
        return json.load(f)



# class FormPage(Page):
#     def __init__(self, page_id, title):
#         super().__init__(page_id, title)

#     def body(self):
#         render_form()

#     def render(self):
#         self.body()





# def render_form():
#     st.write("Please enter the form data:")
#     st.text_input("email:")
        

# main_page = FormPage("main_interface", title="Data Collection Main interface")



