import datetime

import pandas as pd
import pytz
import streamlit as st
from load import connect_to_deta, fetch_all_from_deta_base, init_page

# ----------------------------
# Initialize page
init_page(
    pg_title="Weather",
    pg_icon="⛅",
    title="⛅ Weather",
)

# ----------------------------
# Functions


@st.cache_data(ttl=1800)
def load_weather_data() -> pd.DataFrame:
    """
    Load Weather data from Deta.
    """
    # Load GitHub Contributions data from Deta
    deta = connect_to_deta()
    weather_db = deta.Base("weather")
    weather = fetch_all_from_deta_base(weather_db)

    df = pd.DataFrame(weather).drop(columns=["key"])
    df["dt00"] = pd.to_datetime(df["dt00"], unit="s", utc=True)
    df["sunr"] = pd.to_datetime(df["sunr"], unit="s", utc=True)
    df["suns"] = pd.to_datetime(df["suns"], unit="s", utc=True)
    df["date"] = df["dt00"].dt.tz_convert(pytz.timezone("Asia/Manila"))
    df.sort_values(by="date", inplace=True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    # df = df.set_index("date")

    return df


@st.cache_data(ttl=43200)
def show_sunrise_sunset(df: pd.DataFrame) -> tuple[str, str, str]:
    """
    Show sunrise and sunset times.
    """

    sunrise = df["sunr"][0].tz_convert(pytz.timezone("Asia/Manila"))
    sunset = df["suns"][0].tz_convert(pytz.timezone("Asia/Manila"))
    current_time = datetime.datetime.now(pytz.timezone("Asia/Manila"))

    if current_time < sunrise:
        label = ":sunrise: Sunrise"
        value = sunrise.strftime("%H:%M")
        delta = (df["sunr"][0] - df["sunr"][48] - datetime.timedelta(days=1)).seconds
    elif current_time < sunset:
        label = ":city_sunset: Sunset"
        value = sunset.strftime("%H:%M")
        delta = (df["suns"][0] - df["suns"][48] - datetime.timedelta(days=1)).seconds
    else:
        label = ":city_sunset: Sunset"
        value = sunset.strftime("%H:%M")
        delta = (df["suns"][0] - df["suns"][48] - datetime.timedelta(days=1)).seconds

    return (label, value, delta)


def show_current_weather():
    df = load_weather_data()
    latest_data = df.head(2).copy()
    sunlabel, sunvalue, sundelta = show_sunrise_sunset(df)

    with st.expander("Current Weather", expanded=True):
        st.markdown(
            f"""
            It is currently **{datetime.datetime.strftime(current_time,'%H:%M')}**
            in {latest_data['city'][0]} with **{latest_data['desc'][0]}**.
            The data here was last updated
            **{int((current_time - latest_data['date'][0]).seconds // 60):02}
            minutes ago**.
            """
        )

        mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)

        with mcol1:
            st.markdown(
                f"""
                <img 
                style='margin-top:-1.5em;display:block;
                margin-left:auto;margin-right:auto;' 
                width=150 
                src='http://openweathermap.org/img/wn/{latest_data['icon'][0]}@4x.png'>
                """,
                unsafe_allow_html=True,
            )

        with mcol2:
            st.metric(
                label=":thermometer: Temperature",
                value=f"{round(latest_data['temp'][0]-273.15,2)}°C",
                delta=f"{round(latest_data['temp'][0] - latest_data['temp'][1],2)}°C",
            )

        with mcol3:
            st.metric(
                label=":droplet: Humidity",
                value=f"{round(latest_data['humi'][0]*100,2)}%",
                delta=f"{round((latest_data['humi'][0] - latest_data['humi'][1])*100,2)}%",
            )

        with mcol4:
            st.metric(
                label=":cyclone: Pressure",
                value=f"{round(latest_data['pres'][0],2)} hPa",
                delta=f"{round(latest_data['pres'][0] - latest_data['pres'][1],2)} hPa",
            )

        with mcol5:
            st.metric(
                label=":flags: Wind Speed",
                value=f"{round(latest_data['wvel'][0]*3.6,2)} kph",
                delta=f"{round((latest_data['wvel'][0] - latest_data['wvel'][1])*3.6,2)} kph",
            )

        mcola, mcolb, mcolc, mcold, mcole = st.columns(5)

        with mcola:
            aqi_levels = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
            # aqi_colors = ["#00e400", "#ffff00", "#ff7e00", "#ff0000", "#8f3f97"]

            st.metric(
                label=":smile: Air Quality",
                value=(aqi_levels[latest_data["p_aqi"][0] - 1]),
                delta=f'{latest_data["p_aqi"][0] - latest_data["p_aqi"][1]}Δ: {aqi_levels[latest_data["p_aqi"][1] - 1]}',
            )

        with mcolb:
            st.metric(
                label=":sun_behind_cloud: Cloudiness",
                value=f"{round(latest_data['cldy'][0]*100,2)}%",
                delta=f"{round((latest_data['cldy'][0] - latest_data['cldy'][1])*100,2)}%",
            )

        with mcolc:
            st.metric(
                label=":rain_cloud: Rainfall",
                value=f"{round(latest_data['rain'][0],2)} mm",
                delta=f"{round(latest_data['rain'][0] - latest_data['rain'][1],2)} mm",
                delta_color="inverse",
            )

        with mcold:
            st.metric(label=sunlabel, value=sunvalue, delta=f"{sundelta} seconds")

        with mcole:
            st.metric(
                label=":compass: Wind Direction",
                value=f"{latest_data['wdeg'][0]}°",
                delta=f"{latest_data['wdeg'][0] - latest_data['wdeg'][1]}°",
                help="Measured relative to true North, clockwise",
            )


# ----------------------------
# Global variables

current_time = datetime.datetime.now(pytz.timezone("Asia/Manila"))


# ----------------------------
# Page layout

show_current_weather()
