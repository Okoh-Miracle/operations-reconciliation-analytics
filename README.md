# NexaPay Operations Reconciliation & Performance Analytics

An end-to-end operations analytics project designed to investigate transaction processing performance, reconciliation outcomes, operational exceptions, payment-channel behaviour, and unresolved discrepancies.

Built with **Python, SQL, SQLite, Streamlit, and Plotly**.

---

## Project Overview

NexaPay is a fictional digital payments company processing transactions across multiple payment channels and currencies.

The operations team needs visibility into:

* Transaction processing outcomes
* Reconciliation performance
* Unresolved transactions
* Operational exceptions
* Payment-channel performance
* Processing-time bottlenecks
* Transaction failure patterns
* High-value unresolved transactions
* Currency exposure

This project simulates that operational environment and builds an analytics workflow from raw transaction data through data validation, database analysis, KPI generation, and an interactive operations dashboard.

### End-to-End Workflow

```text
Raw Transaction Data
        ↓
Python Data Cleaning
        ↓
Data Validation
        ↓
SQLite Database
        ↓
SQL Operational Analysis
        ↓
KPI Calculation
        ↓
Streamlit + Plotly Dashboard
        ↓
Operational Insights
```

---

## Dashboard

The dashboard provides an operations-focused view of transaction performance and reconciliation health.

### Key Dashboard Areas

**Operational Overview**

* Total transactions
* Successful transactions
* Success rate
* Reconciliation rate
* Open reconciliation items
* Average processing time
* Critical processing transactions
* Exceptions

**Operations Health**

* Success-rate monitoring
* Reconciliation-rate monitoring
* Transactions resolved
* Unreconciled transactions
* Exception volume
* Total open items

**Transaction & Reconciliation Status**

* Processing status
* Reconciliation status

**Payment Channel Performance**

* Transaction volume by channel
* Success rate by channel

**Processing Efficiency**

* Average processing time by payment channel

**Failure Analysis**

* Failed transaction volume
* Failure reasons

**Transaction Volume Trend**

* Daily transaction activity

**Currency Exposure**

* Transaction volume by currency

**Exception Management**

* Unreconciled transactions
* Exception transactions
* Transaction-level discrepancy review
* High-value unresolved items

---

## Technology Stack

| Technology   | Purpose                                             |
| ------------ | --------------------------------------------------- |
| Python       | Data generation, cleaning, validation and analytics |
| Pandas       | Data manipulation and transformation                |
| NumPy        | Numerical operations                                |
| SQLite       | Relational data storage and SQL analysis            |
| SQL          | Operational analysis and KPI queries                |
| Streamlit    | Interactive dashboard                               |
| Plotly       | Data visualisation                                  |
| Git / GitHub | Version control and portfolio management            |

---

## Data Pipeline

### 1. Data Generation

A synthetic transaction dataset was created to simulate a realistic digital payments operations environment.

The generated dataset includes:

* 1,008 raw transaction records
* 1,000 unique transactions
* Duplicate records
* Missing merchant IDs
* Missing processing times
* Successful, pending and failed transactions
* Multiple payment channels
* Multiple currencies
* Reconciliation outcomes
* Transaction discrepancies
* Failure reasons
* Processing-time anomalies

---

### 2. Data Cleaning

The cleaning pipeline:

* Removes duplicate transaction IDs
* Handles missing merchant IDs
* Handles missing processing times
* Converts numeric fields
* Converts transaction dates
* Recalculates transaction discrepancies
* Classifies processing-time performance
* Produces a clean analytical dataset

Output:

```text
data/clean_transactions.csv
```

---

### 3. Data Validation

The validation process checks eight operational data-quality rules:

1. Transaction IDs are unique
2. Transaction amounts are non-negative
3. Settlement amounts are non-negative
4. Discrepancies are calculated correctly
5. Reconciled transactions have zero discrepancy
6. Failed transactions are not settled
7. Processing times are non-negative
8. Required fields are populated

### Validation Result

```text
Checks passed: 8
Checks failed: 0
Overall result: PASS
```

---

## Database

The project uses SQLite as the analytical database.

### Tables

```text
transactions
merchants
payment_channels
```

The database contains:

* 1,000 transactions
* 10 merchants
* 5 payment channels

Database file:

```text
data/nexapay.db
```

---

## SQL Analysis

The SQL layer investigates operational performance and reconciliation outcomes.

Examples include:

### Transaction Performance

* Total transaction volume
* Successful transactions
* Pending transactions
* Failed transactions
* Success rate

### Reconciliation

* Reconciled transactions
* Unreconciled transactions
* Exception transactions
* Reconciliation rate
* Discrepancy exposure

### Payment Channels

* Transaction volume by channel
* Successful transactions by channel
* Success rate by channel
* Average processing time by channel

### Failure Analysis

* Failure reasons
* Failure frequency
* Operational failure patterns

### Exception Investigation

The analysis also identifies high-value unresolved transactions requiring operational attention.

---

## Key Findings

Using the generated dataset, the analysis identified:

* **1,000** unique transactions
* **65.6%** overall transaction success rate
* **60.3%** reconciliation rate
* **397** unresolved transactions
* **473.82 seconds** average processing time
* **15** transactions with critical processing times above 900 seconds
* **166** failed transactions

The most frequently observed failure reasons included:

* Network Timeout
* System Error
* Insufficient Funds
* Bank Declined
* Fraud Check
* Invalid Account

Payment-channel performance was also compared using transaction volume, success rate, and average processing time.

> Monetary values are kept separated by currency because the dataset contains NGN, USD, GBP and EUR transactions. Cross-currency monetary totals are therefore not treated as a single currency value.

---

## Operational Questions Answered

The project was designed around practical operations questions:

### Transaction Processing

* How many transactions are being processed?
* What percentage succeed?
* Which payment channels have different success patterns?
* Where are processing-time bottlenecks occurring?

### Reconciliation

* How many transactions have been reconciled?
* How many remain unresolved?
* How many are classified as exceptions?
* Which transactions have significant discrepancies?

### Failure Management

* What are the most common failure reasons?
* Which channels experience failed transactions?
* Are there recurring operational patterns?

### Exception Management

* Which transactions remain unresolved?
* Which unresolved transactions have large discrepancies?
* What items should an operations team investigate first?

---

## Project Structure

```text
operations-reconciliation-analytics/
│
├── README.md
│
├── data/
│   ├── raw_transactions.csv
│   ├── clean_transactions.csv
│   ├── merchants.csv
│   ├── payment_channels.csv
│   └── nexapay.db
│
├── docs/
│   └── PROJECT_CASE_STUDY.md
│
├── power-bi/
│   └── dashboard-plan.md
│
├── python/
│   ├── create_database.py
│   ├── dashboard.py
│   ├── data_cleaning.py
│   ├── data_validation.py
│   └── generate_data.py
│
└── sql/
    ├── 01_reconciliation_analysis.sql
    └── 02_kpi_queries.sql
```

---

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Okoh-Miracle/operations-reconciliation-analytics.git
cd operations-reconciliation-analytics
```

### 2. Install the Python dependencies

```bash
python3 -m pip install pandas numpy streamlit plotly pyarrow
```

### 3. Run the dashboard

```bash
python3 -m streamlit run python/dashboard.py
```

Then open:

```text
http://localhost:8501
```

---

## Reproducing the Data Pipeline

To regenerate the synthetic dataset:

```bash
python3 python/generate_data.py
```

Run data cleaning:

```bash
python3 python/data_cleaning.py
```

Run validation:

```bash
python3 python/data_validation.py
```

Create the SQLite database:

```bash
python3 python/create_database.py
```

Run the dashboard:

```bash
python3 -m streamlit run python/dashboard.py
```

---

## Portfolio Context

This project demonstrates an end-to-end approach to operational analytics rather than focusing only on visualisation.

It combines:

**Data Engineering**

* Data generation
* Cleaning
* Validation
* Relational database creation

**Data Analysis**

* SQL queries
* KPI development
* Reconciliation analysis
* Exception investigation

**Operations**

* Transaction monitoring
* Failure analysis
* Processing performance
* Reconciliation management

**Application Development**

* Interactive Streamlit dashboard
* Plotly visualisation
* Filtering and operational drill-down

---

## Future Enhancements

Potential extensions include:

* Automated daily reconciliation jobs
* Real-time transaction monitoring
* API-based transaction ingestion
* Automated exception alerts
* Role-based dashboard views
* SLA monitoring
* Merchant-level performance monitoring
* Automated reporting
* Cloud database deployment
* Production-grade data pipelines
* Anomaly detection using machine learning

---

## Author

**Miracle Okoh**

Technical Operations • Systems Automation • Data & AI

Built as part of a portfolio focused on operational technology, fintech systems, analytics, and intelligent business operations.

