import os

import streamlit as st
from deta import Deta


def init_page(*, pg_title="JSK's Stats", pg_icon=":stars:", title=None, layout="wide"):
    """
    Initialize a streamlit page with a title, icon, and CSS styles.
    """
    st.set_page_config(
        page_title=pg_title,
        page_icon=pg_icon,
        layout=layout,
    )

    # Load CSS styles
    if "css" not in st.session_state:
        st.session_state["css"] = open("assets/style.css").read()
    st.markdown(f"<style>{st.session_state['css']}\n</style>", unsafe_allow_html=True)

    if title:
        st.title(title)


def get_env_var(VAR_NAME: str, from_env: bool = False):
    if os.path.exists(".streamlit/secrets.toml"):
        env_var = st.secrets[VAR_NAME]
    elif from_env:
        env_var = os.environ.get(VAR_NAME)
    else:
        env_var = os.environ.get(VAR_NAME)

    return env_var


# ----------------------------
# Data Functions


@st.experimental_singleton
def connect_to_deta():
    """
    Connect to Deta.
    """
    if "deta" not in st.session_state:
        deta_project_key = get_env_var("DETA_PROJECT_KEY")
        st.session_state["deta"] = Deta(deta_project_key)
    return st.session_state["deta"]


def fetch_all_from_deta_base(deta_base_db):
    """
    Fetch all items from a Deta Base.
    """

    response = deta_base_db.fetch()
    all_items = response.items

    while response.last:
        response = deta_base_db.fetch(last=response.last)
        all_items += response.items
        all_items += response.items

    return all_items
