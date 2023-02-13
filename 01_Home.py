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

    tab1, tab2 = st.tabs(["Description", "An Image"])

    with tab1:
        st.markdown(
            """
        This project is a dashboard that I created to track various statistics
        I have.
        
        I was inspired by [Felix's project](https://howisfelix.today/?) and this
        [Reddit post](https://howisfelix.today/?).

        I wanted to learn Python, data analysis, and data visualization so I
        decided to do a [Quantified Self project](https://quantifiedself.com/)
        to learn these skills.

        This project is a **work in progress**, so I will be adding more pages and
        features as I learn more. I am also planning to add more data sources
        to the dashboard as I go along. So, check back every once in a while
        to see what I have added!

        If you have any suggestions or feedback, please let me know! You can
        contact me on my [Website](https://jskherman.com/about/#contact-me) or
        on [Mastodon](https://mathstodon.xyz/@jskherman).
        """,
            unsafe_allow_html=True,
        )

    with tab2:
        # st.image(
        #     "https://user-images.githubusercontent.com/68434444/201343331-224ed454-e49f-45de-a43a-1de733a7c771.jpg"
        # )

        st.markdown(
            """
        <a href="https://poorlydrawnlines.com/wp-content/uploads/2019/07/keeps-you-going.png" target="_blank">
            <img
                src="https://poorlydrawnlines.com/wp-content/uploads/2019/07/keeps-you-going.png"
                alt="Keeps You Going by Poorly Drawn Lines"
                caption="Keeps You Going by Poorly Drawn Lines"
                width="100%">
        </a>
        """,
            unsafe_allow_html=True,
        )

    # with tab2:
    #     st.image("https://i.imgur.com/P71mNOe.png")

    # with tab3:
    #     st.video("https://www.youtube.com/watch?v=inhxaBLh1Rk")
