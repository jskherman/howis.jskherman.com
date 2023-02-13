import datetime

import calplot
import pandas as pd
import plotly.express as px
import streamlit as st
from load import connect_to_deta, fetch_all_from_deta_base, init_page
from plotly_calplot import calplot as pcalplot

# ----------------------------
# Initialize page
init_page(
    pg_title="GitHub Contributions",
    pg_icon="👨‍💻",
    title="GitHub Contributions",
)

# ----------------------------
# Functions


@st.cache_data(ttl=43200)
def load_github_data() -> tuple[pd.DataFrame, pd.Series]:
    """
    Load GitHub Contributions data from Deta.
    """
    # Load GitHub Contributions data from Deta
    deta = connect_to_deta()
    gh_commits = deta.Base("gh_commits")
    contributions = fetch_all_from_deta_base(gh_commits)

    # Convert to Pandas Series
    ds = pd.Series(
        [c["value"] for c in contributions],
        index=[
            datetime.datetime.strptime(c["date"], "%Y-%m-%d") for c in contributions
        ],
    )

    # Convert to Pandas DataFrame
    df = pd.DataFrame(contributions).drop(columns=["key"])
    df["date"] = df["date"].astype("datetime64[ns]")
    df.sort_values(by="date", inplace=True, ascending=False)

    return (df, ds)


def draw_calplot(ds: pd.Series, year: int = None, cmap: str = "YlGn"):

    if year is not None:
        ds = ds.loc[ds.index.year == year]
        year_labels = False
        title = f"GitHub Contributions in {year}"
    else:
        year_labels = True
        title = "GitHub Contributions"
    fig, ax = calplot.calplot(
        ds,
        how="sum",
        yearascending=False,
        cmap=cmap,
        edgecolor="white",
        linewidth=0.5,
        yearlabels=year_labels,
        suptitle=title,
    )
    return fig


@st.cache_data()
def draw_plotly_calplot(df: pd.DataFrame, year: int = None, cmap: str = "YlGn"):
    if year is not None:
        df = df.loc[df["date"].dt.year == year]
        total_height = 200
        title = f"GitHub Contributions in {year}"
        years_title = False
    else:
        total_height = None
        title = "GitHub Contributions"
        years_title = True

    fig = pcalplot(
        df,
        x="date",
        y="value",
        colorscale=cmap,
        total_height=total_height,
        title=title,
        years_title=years_title,
        name="Contributions",
    )

    return fig


@st.cache_data()
def draw_contrib_heatmap(df_heatmap: pd.DataFrame, cmap: str = "YlGn"):
    df_heatmap["month"] = df_heatmap["date"].dt.month
    df_heatmap["weekday"] = df_heatmap["date"].dt.weekday

    df_heatmap["weekday"] = df_heatmap["weekday"].apply(
        lambda x: datetime.date(1900, 1, x + 1).strftime("%a")
    )
    df_heatmap["month"] = df_heatmap["month"].apply(
        lambda x: datetime.date(1900, x, 1).strftime("%b")
    )

    fig = px.density_heatmap(
        df_heatmap,
        x="month",
        y="weekday",
        z="value",
        histfunc="avg",
        color_continuous_scale=cmap,
    )
    fig.update_yaxes(
        categoryarray=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    )

    fig.update_xaxes(
        categoryarray=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
    )
    fig.update_traces(
        hovertemplate="Month: %{x}<br>Day of the Week: %{y}<br>Mean Contribution: %{z}<extra></extra>",
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="sans-serif"),
    )

    fig.update_layout(
        title="GitHub Contributions Heatmap",
        xaxis_title="Month",
        yaxis_title="Day of the Week",
        font=dict(family="Atkinson Hyperlegible, sans-serif", size=18, color="#7f7f7f"),
        coloraxis=dict(colorbar=dict(title="Mean Contribution")),
    )

    return fig


# ----------------------------
# Global variables

current_year = datetime.datetime.now().year
df, ds = load_github_data()

with st.container():
    ocol1, ocol2 = st.columns(2)

    with ocol1:
        selected_year = st.slider(
            label="Select year in data:",
            min_value=2020,
            max_value=current_year,
            value=current_year,
            step=1,
        )

    with ocol2:
        cmap = st.selectbox(
            label="Select color scheme:",
            options=px.colors.named_colorscales(),
            index=px.colors.named_colorscales().index("ylgn"),
        )


# ----------------------------
# Page Layout

st.markdown("---")


st.plotly_chart(
    draw_plotly_calplot(df, year=selected_year, cmap=cmap),
    use_container_width=True,
)


st.plotly_chart(
    draw_contrib_heatmap(df, cmap=cmap), use_container_width=True, theme="streamlit"
)
