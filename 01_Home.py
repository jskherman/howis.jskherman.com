# ----------------------------
# Imports
import streamlit as st
from load import init_page

# ----------------------------
# Initialize page
init_page(pg_title="JSK's Stats", pg_icon=":stars:", title=":stars: Home")


# ----------------------------
# Main Page

st.markdown(
    """
    ### Welcome to my dashboard!

    This is a dashboard that I created to track various statistics I have.<br>
    Go look at the sidebar for some pages to check out.<br>
    """,
    unsafe_allow_html=True,
)

with st.container():

    tab1, tab2, tab3 = st.tabs(["Drive", "FATE", "lofi"])

    with tab1:
        st.image(
            "https://user-images.githubusercontent.com/68434444/201343331-224ed454-e49f-45de-a43a-1de733a7c771.jpg"
        )

    with tab2:
        st.image("https://i.imgur.com/P71mNOe.png")

    with tab3:
        st.video("https://www.youtube.com/watch?v=inhxaBLh1Rk")
