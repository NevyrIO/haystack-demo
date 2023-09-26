import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

st.write("## Welcome to Gen AI w/ Haystack! 🤖")

st.sidebar.success("Select the demo from the menu above")

st.markdown(
    """
    This **Streamlit** app is a demonstration of how to make Generative AI domain-specific with Haystack.
    
    👈 Choose the demo to the left to experience the app in action. 
    
    *Note: page loading times may be longer on first run*
    """
)
