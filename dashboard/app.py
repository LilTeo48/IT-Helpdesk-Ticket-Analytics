
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# Project configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from database import get_connection


st.set_page_config(
    page_title="IT Help Desk Analytics",
    page_icon="🎫",
    layout="wide"
)


# --------------------------------------------------
# Database connection
# --------------------------------------------------

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


# --------------------------------------------------
# Dashboard header
# --------------------------------------------------

st.title("IT Help Desk Analytics Dashboard")

st.caption(
    "IT support performance, ticket management, "
    "and technician workload analysis"
)


# --------------------------------------------------
# Main dashboard
# --------------------------------------------------

try:

    # Load PostgreSQL data
    df = load_data()

    if df.empty:
        st.warning("No help desk tickets are available.")
        st.stop()

    # --------------------------------------------------
    # Sidebar filters
    # --------------------------------------------------

    st.sidebar.header("Dashboard Filters")

    departments = sorted(df["department"].dropna().unique())
    priorities = sorted(df["priority"].dropna().unique())
    technicians = sorted(df["technician"].dropna().unique())

    selected_departments = st.sidebar.multiselect(
        "Department",
        options=departments,
        default=departments
    )

    selected_priorities = st.sidebar.multiselect(
        "Priority",
        options=priorities,
        default=priorities
    )

    selected_technicians = st.sidebar.multiselect(
        "Technician",
        options=technicians,
        default=technicians
    )

    # Apply filters
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

    # --------------------------------------------------
    # KPI metrics
    # --------------------------------------------------

    st.subheader("Help Desk Overview")

    total_tickets = len(df)

    unfinished = int(
        df["status"].isin(
            ["Open", "In Progress"]
        ).sum()
    )

    completed = int(
        df["status"].isin(
            ["Resolved", "Closed"]
        ).sum()
    )

    completion_rate = (
        completed / total_tickets * 100
        if total_tickets > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Tickets",
        total_tickets
    )

    col2.metric(
        "Unfinished Tickets",
        unfinished
    )

    col3.metric(
        "Resolved / Closed",
        completed
    )

    col4.metric(
        "Completion Rate",
        f"{completion_rate:.1f}%"
    )

    st.divider()

    # --------------------------------------------------
    # Ticket status distribution
    # --------------------------------------------------

    st.subheader("Ticket Status Distribution")

    status_counts = (
        df["status"]
        .value_counts()
        .rename_axis("Status")
        .reset_index(name="Tickets")
    )

    status_order = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    status_chart = px.bar(
        status_counts,
        x="Status",
        y="Tickets",
        color="Status",
        text="Tickets",
        title="Help Desk Tickets by Status",
        category_orders={
            "Status": status_order
        },
        color_discrete_map={
            "Open": "#EF4444",
            "In Progress": "#F59E0B",
            "Resolved": "#3B82F6",
            "Closed": "#22C55E"
        }
    )

    status_chart.update_traces(
        textposition="outside"
    )

    status_chart.update_layout(
        showlegend=False,
        height=450,
        yaxis_range=[
            0,
            max(
                5,
                status_counts["Tickets"].max() * 1.2
            )
        ]
    )

    st.plotly_chart(
        status_chart,
        width="stretch"
    )

    st.divider()

    # --------------------------------------------------
    # Technician workload analysis
    # --------------------------------------------------

    st.subheader("Technician Workload")

    technician_workload = (
        df.assign(
            ticket_group=df["status"].apply(
                lambda status: (
                    "Unfinished"
                    if status in ["Open", "In Progress"]
                    else "Completed"
                )
            )
        )
        .groupby(
            ["technician", "ticket_group"]
        )
        .size()
        .reset_index(name="ticket_count")
    )

    workload_chart = px.bar(
        technician_workload,
        x="technician",
        y="ticket_count",
        color="ticket_group",
        barmode="stack",
        title="Completed vs. Unfinished Tickets by Technician",
        labels={
            "technician": "Technician",
            "ticket_count": "Number of Tickets",
            "ticket_group": "Ticket Status"
        },
        category_orders={
            "ticket_group": [
                "Completed",
                "Unfinished"
            ]
        },
        color_discrete_map={
            "Completed": "#22C55E",
            "Unfinished": "#F59E0B"
        }
    )

    workload_chart.update_layout(
        height=450,
        legend_title_text="Ticket Status"
    )

    st.plotly_chart(
        workload_chart,
        width="stretch"
    )

    st.divider()

    # --------------------------------------------------
    # Department resolution performance
    # --------------------------------------------------

    st.subheader("Department Resolution Performance")

    resolved_tickets = df.dropna(
        subset=["resolution_hours"]
    ).copy()

    resolved_tickets["resolution_hours"] = pd.to_numeric(
        resolved_tickets["resolution_hours"],
        errors="coerce"
    )

    resolved_tickets = resolved_tickets.dropna(
        subset=["resolution_hours"]
    )

    department_resolution = (
        resolved_tickets
        .groupby("department")["resolution_hours"]
        .mean()
        .round(2)
        .reset_index()
        .sort_values(
            "resolution_hours",
            ascending=False
        )
    )

    if department_resolution.empty:

        st.info(
            "No resolved tickets match "
            "the selected filters."
        )

    else:

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
            },
            category_orders={
                "department": department_resolution[
                    "department"
                ].tolist()
            }
        )

        resolution_chart.update_traces(
            textposition="outside",
            texttemplate="%{text:.2f}"
        )

        resolution_chart.update_layout(
            showlegend=False,
            height=450,
            yaxis_title="Average Resolution Time (Hours)"
        )

        st.plotly_chart(
            resolution_chart,
            width="stretch"
        )

    st.divider()

    # --------------------------------------------------
    # Ticket records
    # --------------------------------------------------

    st.subheader("Ticket Records")

    st.caption(
        f"Displaying {len(df)} tickets "
        "based on the selected filters."
    )

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

    # --------------------------------------------------
    # Export filtered data
    # --------------------------------------------------

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Tickets (CSV)",
        data=csv_data,
        file_name="filtered_helpdesk_tickets.csv",
        mime="text/csv"
    )


except Exception as error:

    st.error(
        f"Unable to load dashboard: {error}"
    )
