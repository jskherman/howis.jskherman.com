import datetime

import calplot
import pandas as pd
import plotly.express as px
import polars as pl
import streamlit as st
from load import connect_to_deta, fetch_all_from_deta_base, init_page
from plotly_calplot import calplot as pcalplot

# ----------------------------
# Initialize page
init_page(
    pg_title="Problems Solving",
    pg_icon="👨‍💻",
    title="Problems Solving",
)

# ----------------------------
# Functions


@st.experimental_memo(ttl=43200)
def load_problem_solving_data() -> pl.DataFrame:
    """
    Load Problem Solving data from Deta.
    """
    # Load GitHub Contributions data from Deta
    deta = connect_to_deta()
    problem_solving_db = deta.Base("solve")
    problem_solving = fetch_all_from_deta_base(problem_solving_db)

    df = pl.DataFrame(problem_solving)
    df = df.drop(["event", "type"])
    df = df.with_columns(
        [
            pl.col("timestamp").sort_by(by="timestamp", reverse=True),
        ]
    )
    df = df.with_columns(
        [
            pl.from_epoch("timestamp").cast(pl.Datetime),
        ]
    )

    df = df.with_columns(
        [
            pl.col("timestamp").dt.truncate("1d").cast(pl.Date).alias("Date"),
            pl.col("value").alias("Problems Solved"),
        ]
    )
    df = df.groupby("Date", maintain_order=True).agg(pl.col("Problems Solved").sum())
    date_df = df.to_pandas(date_as_object=False)

    return df, date_df


def generate_streak_info(
    df: pd.DataFrame,
    streak_column: str,
    null_value,
    count_null_streak: bool = False,
) -> pd.DataFrame:
    """
    Parameters
    ----------

    df:
        A dataframe containing a datetime index and a column with a null value
        that corresponds to the end of a streak.

    streak_column:
        The column that contains the streak data.

    null_value:
        The value that indicates the end of a streak.

    Returns
    -------
    final_df:
        A dataframe with the streak information added as a new column.

    Note
    ----
    This function is based on the following post:
    https://joshdevlin.com/blog/calculate-streaks-in-pandas/
    """
    data = df[streak_column].to_frame()
    data["result"] = data[streak_column] != null_value
    if count_null_streak:
        data["start_of_streak"] = data["result"].ne(data["result"].shift())
    else:
        data["start_of_streak"] = (data["result"].ne(data["result"].shift())) + data[
            "result"
        ].eq(False)
    data["streak_id"] = data.start_of_streak.cumsum()
    data[f"{streak_column} Streak"] = data.groupby("streak_id").cumcount() + 1
    final_df = pd.concat([df, data[f"{streak_column} Streak"]], axis=1)
    return final_df


@st.cache()
def draw_plotly_calplot(df: pd.DataFrame, year: int = None):
    if year is not None:
        df = df.loc[df["Date"].dt.year == year]
        total_height = 200
        title = f"Problems Solved in {year}"
        years_title = False
    else:
        total_height = None
        title = "Problems Solved"
        years_title = True

    fig = pcalplot(
        df,
        x="Date",
        y="Problems Solved",
        # colorscale=cmap,
        total_height=total_height,
        title=title,
        years_title=years_title,
        name="Problems Solved",
    )

    return fig


def draw_plotly_bar(df: pd.DataFrame, select_year: int = None):
    if select_year is not None:
        df = df.loc[df["Date"].dt.year == select_year]

    fig = px.bar(df, x="Date", y="Problems Solved", height=400)
    return fig


def solve_metrics(df: pl.DataFrame, count_null_streak: bool = False):
    total_solved = df.select(pl.col("Problems Solved").sum())["Problems Solved"][0]
    avg_solve_perday = round(
        df.select(pl.col("Problems Solved").mean())["Problems Solved"][0], 2
    )

    stdf = df.to_pandas(date_as_object=False)
    stdf = stdf.sort_values(by="Date", ascending=True)
    stdf = stdf.set_index("Date", drop=True)
    stdf = stdf.asfreq("D", fill_value=0)
    stdf = generate_streak_info(
        stdf, "Problems Solved", 0, count_null_streak=count_null_streak
    )
    max_streak = stdf["Problems Solved Streak"].max()
    current_streak = int(stdf["Problems Solved Streak"].iloc[-1])
    # if len(stdf) > 1:
    #     previous_streak = int(stdf["Problems Solved Streak"].iloc[-2])
    # else:
    #     previous_streak = 0

    # streak_delta = current_streak - previous_streak
    # if streak_delta > 0:
    #     streak_delta = f"+{streak_delta}"

    return (
        total_solved,
        avg_solve_perday,
        max_streak,
        current_streak,
        stdf,
    )


# ----------------------------
# Global Variables
current_year = datetime.datetime.now().year
yr_options = list(range(2023, current_year + 1))
yr_options.append(None)
solve_df, date_df = load_problem_solving_data()
(
    total_solved,
    avg_solved,
    max_streak,
    current_streak,
    streak_df,
) = solve_metrics(solve_df, count_null_streak=False)


# selected_year = st.slider(
#     label="Select year in data:",
#     min_value=2022,
#     max_value=current_year,
#     value=current_year,
#     step=1,
# )


# ----------------------------
# Main Page

with st.container():
    pcol1, pcol2 = st.columns([1, 3])

    with pcol1:
        selected_year = st.selectbox(
            label="Select year in data:",
            options=yr_options,
            index=yr_options.index(current_year),
        )

    with pcol2:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("Rationale"):
            st.markdown(
                """
            This page contains a visualizaiton of my problem solving activity.
            I have a hard time getting myself to solve problems on a regular basis,
            so I am trying to track my progress here. I am also trying to get myself
            to solve problems on a daily basis, so I am tracking my progress.
            """
            )

with st.container():
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)

    with mcol1:
        st.metric(
            label="Total Problems Solved",
            value=total_solved,
        )

    with mcol2:
        st.metric(
            label="AVG Solved per Day",
            value=avg_solved,
        )

    with mcol3:
        st.metric(
            label="Max Solving Streak",
            value=max_streak,
        )

    with mcol4:
        st.metric(
            label="Current Solving Streak",
            value=current_streak,
        )

st.markdown("---")

st.plotly_chart(
    draw_plotly_calplot(date_df, year=selected_year),
    use_container_width=True,
)

st.plotly_chart(
    draw_plotly_bar(date_df),
    use_container_width=True,
)
