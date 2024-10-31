import streamlit as st

# Set up page config
st.set_page_config(page_title="Multi-Page Streamlit App", layout="wide", page_icon="🖥")

# Sidebar for navigation
st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
"""
)


