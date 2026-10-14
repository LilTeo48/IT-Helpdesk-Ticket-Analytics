# 🎫 IT Help Desk Ticket Analytics

### Python | PostgreSQL | SQL | Pandas | Plotly | Streamlit

An end-to-end IT help desk analytics project that generates synthetic support ticket data, cleans and validates records, stores tickets in PostgreSQL, and visualizes IT support performance through an interactive Streamlit dashboard.

This project demonstrates practical skills in **Python development, data processing, relational databases, SQL analytics, automated testing, and dashboard development**.

> **Dataset:** 100 synthetic IT support tickets generated for demonstration purposes. No real employee or company data is used.

---

## 📊 Project Overview

IT support teams need visibility into ticket volume, outstanding requests, technician workloads, and resolution performance.

This project simulates a help desk ticket management environment and provides an analytics solution to answer questions such as:

- How many support tickets are currently unfinished?
- What percentage of tickets have been resolved or closed?
- Which technicians have the largest outstanding workloads?
- Which departments experience longer average resolution times?
- How does ticket priority affect the distribution of support requests?

The dashboard enables users to explore these metrics using interactive filters.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.13 | Application development and data processing |
| Pandas | Data cleaning, validation, and analysis |
| Faker | Synthetic ticket data generation |
| PostgreSQL 18 | Relational database storage |
| SQL | Analytical queries and aggregations |
| Psycopg 3 | Python-to-PostgreSQL connectivity |
| Streamlit | Interactive web dashboard |
| Plotly | Interactive data visualizations |
| Pytest | Automated data-cleaning tests |
| Git & GitHub | Version control and project documentation |

## 🏗️ Project Architecture

The project follows a data pipeline that transforms generated support tickets into actionable analytics.

```text
Synthetic Ticket Generation
          |
          v
Raw CSV Dataset
          |
          v
Python / Pandas Data Cleaning
          |
          v
Cleaned CSV Dataset
          |
          v
PostgreSQL Database
          |
          +------> SQL Analytics
          |
          v
Streamlit Dashboard
          |
          v
Interactive Charts, KPIs & CSV Export
```

## 📁 Project Structure

```text
IT-Helpdesk-Ticket-Analytics/
|
|-- dashboard/
|   |-- app.py
|
|-- data/
|   |-- raw/
|   |-- processed/
|
|-- sql/
|   |-- schema.sql
|   |-- analytics.sql
|
|-- src/
|   |-- generate_tickets.py
|   |-- clean_tickets.py
|   |-- database.py
|   |-- load_tickets.py
|
|-- tests/
|   |-- test_clean_tickets.py
|
|-- .gitignore
|-- requirements.txt
|-- README.md
```

Generated CSV datasets are excluded from Git version control.

## ✨ Key Features

### 1. Synthetic Data Generation

Generates realistic sample IT help desk records containing:

- Ticket ID
- Employee name
- Department
- Issue category
- Priority level
- Ticket status
- Assigned technician
- Ticket creation timestamp
- Resolution timestamp
- Resolution duration in hours

### 2. Data Cleaning and Validation

Uses Pandas to prepare ticket records for analysis.

The cleaning pipeline includes duplicate removal, status validation, timestamp validation, and resolution-duration calculations.

Unresolved tickets retain missing resolution timestamps and durations because those values are not yet available.

### 3. PostgreSQL Database Integration

Stores cleaned ticket records in a relational PostgreSQL database.

The database schema includes:

- Primary key constraints
- Required fields
- Valid ticket priority values
- Valid ticket status values
- Resolution date validation
- Nonnegative resolution-duration validation

Python scripts provide database connectivity and ticket-loading functionality.

### 4. SQL Analytics

The project includes SQL queries for:

- Total ticket count
- Ticket distribution by status
- Ticket distribution by priority
- Average resolution time by department
- Technician workload and unfinished ticket counts

### 5. Interactive Streamlit Dashboard

The dashboard includes:

**Help Desk Overview**
- Total tickets
- Unfinished tickets
- Resolved or closed tickets
- Ticket completion rate

**Ticket Status Distribution**
- Interactive bar chart showing ticket counts by status

**Technician Workload**
- Stacked bar chart comparing completed and unfinished tickets

**Department Resolution Performance**
- Average ticket resolution time by department

**Interactive Filters**
- Department
- Priority
- Technician

**Ticket Records and Export**
- Filtered ticket table
- CSV download of selected records

## 📈 Sample Analytics Results

The following results are based on the project's 100-ticket synthetic dataset.

### Ticket Summary

| Metric | Value |
|---|---:|
| Total tickets | 100 |
| Open | 30 |
| In Progress | 24 |
| Resolved | 18 |
| Closed | 28 |
| Unfinished tickets | 54 |
| Completed tickets | 46 |
| Completion rate | 46.0% |

### Technician Workload

| Technician | Assigned | Unfinished | Completed |
|---|---:|---:|---:|
| Alex Johnson | 22 | 13 | 9 |
| Casey Davis | 27 | 12 | 15 |
| Morgan Lee | 26 | 14 | 12 |
| Taylor Brooks | 25 | 15 | 10 |

### Average Resolution Time by Department

| Department | Average Hours |
|---|---:|
| Sales | 52.70 |
| IT | 45.67 |
| Human Resources | 37.64 |
| Operations | 36.25 |
| Finance | 35.09 |

These results illustrate how ticket analytics can help identify potential workload imbalances and areas requiring further investigation. They are simulated findings, not measurements of an actual IT organization.

## 🚀 Installation and Setup

### Prerequisites

- Python 3.13
- PostgreSQL
- Git
- A terminal or Python IDE such as PyCharm

### 1. Clone the Repository

```bash
git clone https://github.com/LilTeo48/IT-Helpdesk-Ticket-Analytics.git
cd IT-Helpdesk-Ticket-Analytics
```

### 2. Install Python Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 3. Generate Synthetic Ticket Data

```bash
python3 src/generate_tickets.py
```

This creates the raw ticket dataset.

### 4. Clean the Ticket Data

```bash
python3 src/clean_tickets.py
```

This creates the processed ticket dataset.

### 5. Create the PostgreSQL Database

Start your local PostgreSQL server, then create the database:

```bash
createdb -U "$(whoami)" helpdesk_analytics
```

This command assumes PostgreSQL is configured with a local role matching your macOS username.

### 6. Create the Database Table

```bash
psql -U "$(whoami)" -d helpdesk_analytics -v ON_ERROR_STOP=1 -f sql/schema.sql
```

### 7. Load the Ticket Data

```bash
python3 src/load_tickets.py
```

The Python database configuration must match your local PostgreSQL installation.

### 8. Run SQL Analytics

```bash
psql -U "$(whoami)" -d helpdesk_analytics -v ON_ERROR_STOP=1 -f sql/analytics.sql
```

### 9. Launch the Dashboard

```bash
python3 -m streamlit run dashboard/app.py
```

Open the local address provided by Streamlit, typically:

http://localhost:8501

## 🧪 Automated Testing

The project uses Pytest to validate data-cleaning behavior.

Run:

```bash
python3 -m pytest tests/ -v
```

The existing test suite covers:

1. Ticket counts
2. Resolution duration calculations
3. Unresolved ticket handling
4. Duplicate removal
5. Invalid ticket statuses
6. Invalid resolution dates

**Latest local test result: 6 passed.**

## 📸 Dashboard Screenshots

Dashboard screenshots can be added here to demonstrate the application visually.

Recommended screenshots:

- Help Desk Overview and Ticket Status Distribution
- Technician Workload
- Department Resolution Performance
- Interactive Filters and Ticket Records

## 💡 Skills Demonstrated

- Building a multi-stage Python data pipeline
- Cleaning and validating structured datasets
- Designing a PostgreSQL relational database
- Writing SQL queries for operational analytics
- Integrating Python applications with PostgreSQL
- Creating interactive dashboards using Streamlit and Plotly
- Writing automated tests using Pytest
- Managing source code with Git and GitHub
- Documenting technical projects for reproducibility

## 🔮 Potential Future Improvements

- Add ticket creation and resolution trends over time
- Introduce service-level agreement (SLA) metrics
- Add ticket aging and overdue ticket analysis
- Expand automated tests to cover database loading and dashboard calculations
- Deploy the dashboard with a hosted PostgreSQL database
- Add automated data refresh and scheduled reporting

## 📌 Project Status

**Functional local prototype — portfolio documentation in progress.**

Completed components include synthetic data generation, data cleaning, PostgreSQL integration, SQL analytics, automated data-cleaning tests, and an interactive Streamlit dashboard.

## 👨‍💻 Author

**Tyler Chadwick**

GitHub: [LilTeo48](https://github.com/LilTeo48)

Project Repository: [IT Help Desk Ticket Analytics](https://github.com/LilTeo48/IT-Helpdesk-Ticket-Analytics)