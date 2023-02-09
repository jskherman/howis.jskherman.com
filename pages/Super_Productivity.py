# Imports
import datetime
import json

import dropbox
import pandas as pd
import pytz
import streamlit as st
from load import init_page

# Initialize the page
init_page(pg_title="Super Productivity", pg_icon="✅", title="Super Productivity")

# ---------------------------------------------
# Functions
@st.experimental_singleton
def connect_to_dropbox():
    """
    Connect to Dropbox.
    """
    if "dbx" not in st.session_state:
        st.session_state["dbx"] = dropbox.Dropbox(
            st.secrets["data"]["dropbox_access_token"]
        )
    return st.session_state["dbx"]


@st.experimental_memo()
def get_sp_data() -> dict:
    """
    Gets the data from the Super Productivity JSON file on Dropbox
    """
    dbx = connect_to_dropbox()
    _metadata, result = dbx.files_download(path="/super_productivity/sp.json")
    data = json.loads(result.content)
    return data


def unix_to_local(unix_time: int, timezone="Asia/Manila") -> datetime.datetime:
    """
    Converts unix time to local time given a timezone.
    """
    timestamp = datetime.datetime.utcfromtimestamp(unix_time)
    timestamp = timestamp.replace(tzinfo=pytz.timezone("UTC")).astimezone(
        pytz.timezone(timezone)
    )
    return timestamp


def munix_to_local(munix_time: int, timezone="Asia/Manila") -> datetime.datetime:
    """
    Converts unix time in milliseconds to local time given a timezone.
    """
    timestamp = datetime.datetime.utcfromtimestamp(munix_time // 1000)
    timestamp = timestamp.replace(tzinfo=pytz.timezone("UTC")).astimezone(
        pytz.timezone(timezone)
    )
    return timestamp


def get_sptask_info(sp_data: dict, task_id: str, tasklist: str) -> dict:
    """
    Gets the metadata of a task from the Super Productivity JSON file.
    """

    # Get task metadata

    # Task Title
    title = sp_data[tasklist]["entities"][task_id]["title"]

    # Task Project
    project = sp_data["project"]["entities"][
        (sp_data[tasklist]["entities"][task_id]["projectId"])
    ]["title"]

    # Task Status
    if sp_data[tasklist]["entities"][task_id]["isDone"]:
        status = True
    else:
        status = False

    # Task Creation Date
    created = munix_to_local(sp_data[tasklist]["entities"][task_id]["created"])

    # Task Completion Date
    if sp_data[tasklist]["entities"][task_id]["doneOn"] is None:
        completion = None
    else:
        completion = munix_to_local(sp_data[tasklist]["entities"][task_id]["doneOn"])

    # Task Time Spent
    spent = sp_data[tasklist]["entities"][task_id]["timeSpent"] // 1000

    # Task Time Estimate
    estimate = sp_data[tasklist]["entities"][task_id]["timeEstimate"] // 1000

    # Task Fudge Ratio
    if estimate > 0:
        fudge_ratio = round(spent / estimate, 2)
    else:
        fudge_ratio = 0

    # Get tags for Task
    tags = []
    for tag_id in sp_data[tasklist]["entities"][task_id]["tagIds"]:
        tag = sp_data["tag"]["entities"][tag_id]["title"]
        tags.append(tag)

    # Get Priority of task
    if "A" in tags:
        priority = 4
    elif "B" in tags:
        priority = 3
    elif "C" in tags:
        priority = 2
    else:
        priority = 1

    if "Today" in tags:
        tags.remove("Today")

    # Create dictionary of task metadata
    task_metadata = {
        "title": title,
        "project": project,
        "status": status,
        "priority": priority,
        "created_on": created,
        "completed_on": completion,
        "time_spent": spent,
        "time_estimate": estimate,
        "fudge_ratio": fudge_ratio,
        "tags": tags,
    }

    return task_metadata


@st.experimental_memo()
def get_sptasks(sp_data: dict):
    """
    Gets all tasks from the Super Productivity JSON file.
    """
    tasks = []
    for task in sp_data["task"]["entities"]:
        task_meta = get_sptask_info(sp_data, task, tasklist="task")
        tasks.append(task_meta)

    for task in sp_data["taskArchive"]["entities"]:
        task_meta = get_sptask_info(sp_data, task, tasklist="taskArchive")
        tasks.append(task_meta)

    df_tasks = pd.DataFrame(tasks)
    df_tasks = df_tasks[
        [
            "status",
            "priority",
            "title",
            "project",
            "created_on",
            "completed_on",
            "time_spent",
            "time_estimate",
            "fudge_ratio",
            "tags",
        ]
    ]

    df_tasks.rename(
        columns={
            "status": "Status",
            "priority": "Priority",
            "title": "Title",
            "project": "Project",
            "created_on": "Created On",
            "completed_on": "Completed On",
            "time_spent": "Time Spent",
            "time_estimate": "Time Estimate",
            "fudge_ratio": "Fudge Ratio",
            "tags": "Tags",
        },
        inplace=True,
    )

    return df_tasks


# ---------------------------------------------
# Global variables
df_tasks = get_sptasks(get_sp_data())
df_done = df_tasks[df_tasks["Status"] == True]
df_recent = df_done[
    df_done["Completed On"].dt.date > datetime.date.today() - datetime.timedelta(days=7)
]

# ---------------------------------------------
# Page layout

with st.container():
    st.markdown("### Recently Completed")
    st.dataframe(df_recent)
