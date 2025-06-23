import streamlit as st


def get_google_api_key():
    # Ensure the user has set the API key in .streamlit/secrets.toml
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error(
            "Google API key not found. Please set it in .streamlit/secrets.toml as GOOGLE_API_KEY.")
        st.stop()  # Stop the app if the key is not found
    return st.secrets["GOOGLE_API_KEY"]
