import streamlit as st

def draw_main_page():
    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
        .big-font {
            font-size:80px !important;
            font-family: Arial !important;
            text-align: center !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Hello World !!</p>', unsafe_allow_html=True)   

draw_main_page()