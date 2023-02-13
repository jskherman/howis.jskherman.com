import base64
import datetime
import random
import string

import pytz
import streamlit as st
from load import connect_to_deta, init_page

# ----------------------------
# Initialize page
init_page(
    pg_title="Trackers",
    pg_icon="📈",
    title="Trackers",
)

# ----------------------------
# Functions
def gen_timestamp_key():
    """
    Generate a timestamp key for Deta Base.
    """
    key = datetime.datetime.now(pytz.timezone(timezone)).strftime("%Y%m%d%H%M%S")
    key += random.choice(string.ascii_letters)
    key += random.choice(string.ascii_letters)
    return key


@st.cache_resource
def initialize_db():
    deta = connect_to_deta()
    events_db = deta.Base("events")
    habits_db = deta.Base("habits")
    solve_db = deta.Base("solve")

    return events_db, habits_db, solve_db


# ----------------------------
# Global Variables

events_db, habits_db, solve_db = initialize_db()

# ----------------------------
# Page Layout

# Settings
with st.sidebar:
    with st.expander("**Settings** ⚙"):
        audio_on = st.checkbox("🔊 **Fanfare?**", value=True)

        timezone = st.selectbox(
            "🌏 Select your preferred timezone:",
            options=pytz.all_timezones,
            index=pytz.all_timezones.index("Asia/Manila"),
        )

    # Current Date and Time
    with st.container():

        date_input = st.date_input(
            "Event Date (YYYY/MM/DD)",
            value=datetime.datetime.now(pytz.timezone(timezone)),
        )

        time_input = st.time_input(
            "Event Time (24-hr format)",
            value=datetime.datetime.now(pytz.timezone(timezone)),
        )

if audio_on:
    # Fanfare config
    fanfare_file = open("assets/fanfare.mp3", "rb")
    fanfare_html = f'\n<audio autoplay class="stAudio">\n<source src="data:audio/ogg;base64,{(base64.b64encode(fanfare_file.read()).decode())}" type="audio/mp3">\nYour browser does not support the audio element.\n</audio>'
else:
    fanfare_html = ""

datetime_input = datetime.datetime.combine(date_input, time_input)
unix_timestamp = datetime_input.timestamp() + random.randint(0, 9)

# ----------------------------
# Main Section: Event and Habit Trackers

# f"generated key: {gen_timestamp_key()}"

events_tab, habits_tab = st.tabs(["Events", "Habits"])

# Event Trackers
with events_tab:

    ### Events Row 1 ###
    with st.container():
        event_r1c1, event_r1c2, event_r1c3 = st.columns(3)

        with event_r1c1:
            urge_form = st.form(key="t_urge")
            with urge_form:
                st.markdown("##### Felt Urge 😖")
                if st.form_submit_button("Submit", type="primary"):
                    events_db.put(
                        {
                            "key": gen_timestamp_key(),
                            "event": "felt horny",
                            "type": "event",
                            "value": 1,
                            "timestamp": unix_timestamp,
                        }
                    )
                    st.snow()

        with event_r1c2:
            distracted_form = st.form(key="t_distraction")
            with distracted_form:
                st.markdown("##### Got Distracted 😐")
                if distracted_form.form_submit_button("Submit", type="primary"):
                    events_db.put(
                        {
                            "key": gen_timestamp_key(),
                            "event": "got distracted",
                            "type": "event",
                            "value": 1,
                            "timestamp": unix_timestamp,
                        }
                    )
                    st.snow()

    ### Events Row 2 ###
    with st.container():
        event_r2c1, event_r2c2, event_r2c3 = st.columns(3)

        with event_r2c1:
            wake_form = st.form(key="t_wake")
            with wake_form:
                st.markdown("##### Woke Up 🌞")
                if wake_form.form_submit_button("Submit", type="primary"):
                    events_db.put(
                        {
                            "key": gen_timestamp_key(),
                            "event": "wake up",
                            "type": "event",
                            "value": 1,
                            "timestamp": unix_timestamp,
                        }
                    )
                    st.markdown(fanfare_html, unsafe_allow_html=True)
                    st.balloons()

        with event_r2c2:
            sleep_form = st.form(key="t_sleep")
            with sleep_form:
                st.markdown("##### Sleep 🌒")
                if sleep_form.form_submit_button("Submit", type="primary"):
                    events_db.put(
                        {
                            "key": gen_timestamp_key(),
                            "event": "sleep",
                            "type": "event",
                            "value": 1,
                            "timestamp": unix_timestamp,
                        }
                    )
                    st.markdown(fanfare_html, unsafe_allow_html=True)
                    st.balloons()

    with st.container():
        event_r3c1, event_r3c2, event_r3c3 = st.columns(3)

        with event_r3c1:
            hungry_form = st.form(key="t_hungry")
            with hungry_form:
                st.markdown("##### Felt Hungry 🍖")
                if hungry_form.form_submit_button("Submit", type="primary"):
                    events_db.put(
                        {
                            "key": gen_timestamp_key(),
                            "event": "felt hungry",
                            "type": "event",
                            "value": 1,
                            "timestamp": unix_timestamp,
                        }
                    )
                    st.snow()

        with event_r3c2:
            poop_form = st.form(key="t_poop")
            with poop_form:
                st.markdown("##### Defecated 💩")
                if poop_form.form_submit_button("Submit", type="primary"):
                    events_db.put(
                        {
                            "key": gen_timestamp_key(),
                            "event": "defecated",
                            "type": "event",
                            "value": 1,
                            "timestamp": unix_timestamp,
                        }
                    )
                    st.markdown(fanfare_html, unsafe_allow_html=True)
                    st.balloons()

        with event_r3c3:
            urinate_form = st.form(key="t_urinate")
            with urinate_form:
                st.markdown("##### Urinate 💦")
                if urinate_form.form_submit_button("Submit", type="primary"):
                    events_db.put(
                        {
                            "key": gen_timestamp_key(),
                            "event": "urinate",
                            "type": "event",
                            "value": 1,
                            "timestamp": unix_timestamp,
                        }
                    )
                    st.markdown(fanfare_html, unsafe_allow_html=True)
                    st.balloons()

# Habit Trackers
with habits_tab:

    ### Habits Row 1 ###
    with st.container():
        habit_r1c1, habit_r1c2, habit_r1c3 = st.columns(3)

        with habit_r1c1:
            morale_form = st.form(key="h_morale")
            with morale_form:
                st.markdown("##### Morale 🎃")
                morale = morale_form.selectbox(
                    "Value", options=[4, 2, 0, -2, -4], index=2
                )
                if morale_form.form_submit_button("Submit", type="primary"):
                    habits_db.put(
                        {
                            "key": gen_timestamp_key(),
                            "event": "morale",
                            "type": "habit",
                            "value": morale,
                            "timestamp": unix_timestamp,
                        }
                    )
                    st.markdown(fanfare_html, unsafe_allow_html=True)
                    st.balloons()

        with habit_r1c2:
            journal_form = st.form(key="h_journaling")
            with journal_form:
                st.markdown("##### Journal 📝")
                journal = journal_form.number_input(
                    "Value", min_value=0.0, max_value=1.0, step=0.1, value=1.0
                )
                if journal_form.form_submit_button("Submit", type="primary"):
                    habits_db.put(
                        {
                            "key": gen_timestamp_key(),
                            "event": "journaling",
                            "type": "habit",
                            "value": journal,
                            "timestamp": unix_timestamp,
                        }
                    )
                    st.markdown(fanfare_html, unsafe_allow_html=True)
                    st.balloons()

        with habit_r1c3:
            water_form = st.form(key="h_water", clear_on_submit=True)
            with water_form:
                st.markdown("##### Drink Water 💧")
                water = water_form.number_input(
                    "Number of Glasses", min_value=1, step=1
                )
                if water_form.form_submit_button("Submit", type="primary"):
                    habits_db.put(
                        {
                            "key": gen_timestamp_key(),
                            "event": "drink water",
                            "type": "habit",
                            "value": water,
                            "timestamp": unix_timestamp,
                        }
                    )
                    st.markdown(fanfare_html, unsafe_allow_html=True)
                    st.balloons()

    ### Habits Row 2 ###
    with st.container():
        habit_r2c1, habit_r2c2, habit_r1c3 = st.columns(3)

        with habit_r2c1:
            solve_form = st.form(key="h_solve", clear_on_submit=True)
            with solve_form:
                st.markdown("##### Solve Problems 🧠")
                solvep = solve_form.number_input(
                    "Number of Problems Solved", min_value=1, step=1
                )
                if solve_form.form_submit_button("Submit", type="primary"):
                    solve_db.put(
                        {
                            "key": gen_timestamp_key(),
                            "event": "solve problem",
                            "type": "habit",
                            "value": solvep,
                            "timestamp": unix_timestamp,
                        }
                    )
                    st.markdown(fanfare_html, unsafe_allow_html=True)
                    st.balloons()
