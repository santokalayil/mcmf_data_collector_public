import json
import streamlit.components.v1 as components
import streamlit as st
from ...paths import FOOTER_COMPONENTS_DIR
from . import INFO




# @st.cache
def draw(height=600, scrolling=False):
    html_path = FOOTER_COMPONENTS_DIR / "element.html"
    js_path = FOOTER_COMPONENTS_DIR / "script.js"
    css_path = FOOTER_COMPONENTS_DIR / "style.css"

    version_info = INFO["version"]

    
    with open(css_path, 'r') as f:
        css_style = "".join([line.strip() for line in f.readlines() if line.strip()])

    js_injection_text = open(js_path).read().replace("__CUSTOM_CSS__", css_style)
    js_html = f"<script>\n{js_injection_text}\n</script>"
    html_text = open(html_path).read().replace("<< __VERSION_INFO__ >>", version_info)

    contents = html_text + "\n" + js_html

    components.html(contents,
        height=height,
        scrolling=scrolling,
    )