
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Allow imports from the src folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from database import get_connection


st.set_page_config(
    page_title="IT Help Desk Analytics",
    page_icon="🎫",
    layout="wide"
)


@st.cache_data(ttl=60)
def load_data():
    """Retrieve help desk tickets from PostgreSQL."""

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM helpdesk_tickets
                ORDER BY ticket_id;
            """)

            rows = cursor.fetchall()
            columns = [
                column.name
                for column in cursor.description
            ]

    return pd.DataFrame(rows, columns=columns)


st.title("IT Help Desk Analytics Dashboard")
st.caption("IT support performance and ticket management")


try:
    df = load_data()


    # Interactive sidebar filters
    st.sidebar.header("Dashboard Filters")

    selected_departments = st.sidebar.multiselect(
        "Department",
        options=sorted(df["department"].unique()),
        default=sorted(df["department"].unique())
    )

    selected_priorities = st.sidebar.multiselect(
        "Priority",
        options=sorted(df["priority"].unique()),
        default=sorted(df["priority"].unique())
    )

    selected_technicians = st.sidebar.multiselect(
        "Technician",
        options=sorted(df["technician"].unique()),
        default=sorted(df["technician"].unique())
    )

    # Apply filters to all dashboard metrics and charts
    df = df[
        df["department"].isin(selected_departments)
        & df["priority"].isin(selected_priorities)
        & df["technician"].isin(selected_technicians)
    ].copy()

    if df.empty:
        st.warning(
            "No tickets match the selected filters. "
            "Try adjusting your selections."
        )
        st.stop()


    # Dashboard KPI metrics
    total_tickets = len(df)

    unfinished = df["status"].isin(
        ["Open", "In Progress"]
    ).sum()

    completed = df["status"].isin(
        ["Resolved", "Closed"]
    ).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tickets", total_tickets)
    col2.metric("Unfinished Tickets", unfinished)
    col3.metric("Resolved / Closed", completed)

    # Ticket status chart
    st.subheader("Ticket Status Distribution")

    status_counts = (
        df["status"]
        .value_counts()
        .rename_axis("Status")
        .reset_index(name="Tickets")
    )

    fig = px.bar(
        status_counts,
        x="Status",
        y="Tickets",
        color="Status",
        text="Tickets",
        title="Help Desk Tickets by Status"
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        showlegend=False,
        yaxis_range=[
            0,
            max(5, status_counts["Tickets"].max() * 1.2)
        ] if not status_counts.empty else [0, 5],
        height=450
    )

    st.plotly_chart(fig, width="stretch")


    # Technician workload analysis
    st.subheader("Technician Workload")

    technician_workload = (
        df.groupby("technician")
        .agg(
            assigned_tickets=("ticket_id", "count"),
            unfinished_tickets=(
                "status",
                lambda statuses: statuses.isin(
                    ["Open", "In Progress"]
                ).sum()
            )
        )
        .reset_index()
    )

    workload_chart = px.bar(
        technician_workload,
        x="technician",
        y=["assigned_tickets", "unfinished_tickets"],
        barmode="group",
        title="Tickets Assigned vs. Unfinished by Technician",
        labels={
            "technician": "Technician",
            "value": "Number of Tickets",
            "variable": "Ticket Metric"
        }
    )

    workload_chart.update_layout(height=450)

    st.plotly_chart(workload_chart, width="stretch")


    # Average resolution time by department
    st.subheader("Department Resolution Performance")

    resolved_tickets = df.dropna(
        subset=["resolution_hours"]
    ).copy()

    resolved_tickets["resolution_hours"] = pd.to_numeric(
        resolved_tickets["resolution_hours"]
    )

    department_resolution = (
        resolved_tickets.groupby("department")[
            "resolution_hours"
        ]
        .mean()
        .round(2)
        .reset_index()
        .sort_values(
            "resolution_hours",
            ascending=False
        )
    )

    resolution_chart = px.bar(
        department_resolution,
        x="department",
        y="resolution_hours",
        color="department",
        text="resolution_hours",
        title="Average Ticket Resolution Time by Department",
        labels={
            "department": "Department",
            "resolution_hours": "Average Resolution Time (Hours)"
        }
    )

    resolution_chart.update_traces(
        textposition="outside",
        texttemplate="%{text:.2f}"
    )

    resolution_chart.update_layout(
        showlegend=False,
        height=450
    )

    st.plotly_chart(resolution_chart, width="stretch")



    # Display ticket records
    st.subheader("Ticket Records")
    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )


except Exception as error:
    st.error(f"Unable to load dashboard: {error}")
