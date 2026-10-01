import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NexaPay Operations Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b1118;
        color: #f5f7fa;
    }

    [data-testid="stSidebar"] {
        background-color: #0a1016;
        border-right: 1px solid #202b37;
    }

    [data-testid="stSidebar"] * {
        color: #d8e0e8;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: #f5f7fa !important;
    }

    .hero {
        background-color: #111923;
        border: 1px solid #202b37;
        border-radius: 14px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
    }

    .hero-eyebrow {
        color: #54d6c7;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        margin-bottom: 0.45rem;
    }

    .hero-title {
        color: #f5f7fa;
        font-size: 2rem;
        font-weight: 750;
        margin-bottom: 0.35rem;
    }

    .hero-subtitle {
        color: #8f9cab;
        font-size: 0.95rem;
    }

    .status-pill {
        display: inline-block;
        background-color: #102822;
        border: 1px solid #1d5148;
        color: #54d6c7;
        border-radius: 20px;
        padding: 0.35rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .section-heading {
        color: #f5f7fa;
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 1.8rem;
        margin-bottom: 0.2rem;
    }

    .section-subtitle {
        color: #7f8c9b;
        font-size: 0.82rem;
        margin-bottom: 0.9rem;
    }

    .kpi-card {
        background-color: #111923;
        border: 1px solid #202b37;
        border-radius: 12px;
        padding: 1rem;
        min-height: 105px;
    }

    .kpi-label {
        color: #8794a3;
        font-size: 0.75rem;
        margin-bottom: 0.35rem;
    }

    .kpi-value {
        color: #f5f7fa;
        font-size: 1.55rem;
        font-weight: 750;
    }

    .kpi-accent {
        color: #54d6c7;
    }

    .small-note {
        color: #718090;
        font-size: 0.75rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():

    transactions = pd.read_csv(
        "data/clean_transactions.csv"
    )

    merchants = pd.read_csv(
        "data/merchants.csv"
    )

    transactions["transaction_date"] = pd.to_datetime(
        transactions["transaction_date"],
        errors="coerce"
    )

    merchant_columns = [
        "merchant_id",
        "merchant_name",
        "industry"
    ]

    merchants = merchants[
        [col for col in merchant_columns if col in merchants.columns]
    ]

    transactions = transactions.drop(
        columns=["merchant_name", "industry"],
        errors="ignore"
    )

    transactions = transactions.merge(
        merchants,
        on="merchant_id",
        how="left"
    )

    if "merchant_name" in transactions.columns:
        transactions["merchant_name"] = (
            transactions["merchant_name"]
            .fillna("Unknown Merchant")
        )

    if "industry" in transactions.columns:
        transactions["industry"] = (
            transactions["industry"]
            .fillna("Unknown")
        )

    return transactions


df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## NEXAPAY")

    st.caption("OPERATIONS CONSOLE")

    st.divider()

    st.markdown("### Dashboard Filters")

    currencies = sorted(
        df["currency"].dropna().unique().tolist()
    )

    selected_currencies = st.multiselect(
        "Currency",
        currencies,
        default=currencies
    )

    channels = sorted(
        df["payment_channel"].dropna().unique().tolist()
    )

    selected_channels = st.multiselect(
        "Payment Channel",
        channels,
        default=channels
    )

    statuses = sorted(
        df["processing_status"].dropna().unique().tolist()
    )

    selected_statuses = st.multiselect(
        "Processing Status",
        statuses,
        default=statuses
    )

    st.divider()

    st.caption("Dataset")
    st.markdown("**NexaPay Transactions**")
    st.caption(f"{len(df):,} cleaned records")

    st.markdown(
        '<span class="status-pill">● DATASET ACTIVE</span>',
        unsafe_allow_html=True
    )


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    df["currency"].isin(selected_currencies)
    & df["payment_channel"].isin(selected_channels)
    & df["processing_status"].isin(selected_statuses)
].copy()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_transactions = len(filtered_df)

successful_transactions = (
    filtered_df["processing_status"]
    .eq("Successful")
    .sum()
)

success_rate = (
    successful_transactions / total_transactions * 100
    if total_transactions
    else 0
)

reconciled_transactions = (
    filtered_df["reconciliation_status"]
    .eq("Reconciled")
    .sum()
)

reconciliation_rate = (
    reconciled_transactions / total_transactions * 100
    if total_transactions
    else 0
)

unreconciled = (
    filtered_df["reconciliation_status"]
    .eq("Unreconciled")
    .sum()
)

exceptions = (
    filtered_df["reconciliation_status"]
    .eq("Exception")
    .sum()
)

unresolved_transactions = (
    unreconciled + exceptions
)

avg_processing_time = (
    filtered_df["processing_time_seconds"].mean()
    if total_transactions
    else 0
)

critical_processing = (
    filtered_df["processing_time_seconds"]
    .gt(900)
    .sum()
)


# ============================================================
# HERO
# ============================================================

st.markdown("## NEXAPAY • OPERATIONS INTELLIGENCE")

st.markdown(
    "# Transaction Operations Dashboard"
)

st.caption(
    "Monitor transaction processing, reconciliation performance, "
    "operational exceptions and payment-channel behaviour."
)

st.divider()

# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-heading">Operational Overview</div>',
    unsafe_allow_html=True
)

st.caption(
    "Core transaction processing and reconciliation indicators."
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Total Transactions",
        f"{total_transactions:,}"
    )

with k2:
    st.metric(
        "Success Rate",
        f"{success_rate:.1f}%"
    )

with k3:
    st.metric(
        "Reconciliation Rate",
        f"{reconciliation_rate:.1f}%"
    )

with k4:
    st.metric(
        "Open Reconciliation Items",
        f"{unresolved_transactions:,}"
    )


k5, k6, k7, k8 = st.columns(4)

with k5:
    st.metric(
        "Successful Transactions",
        f"{successful_transactions:,}"
    )

with k6:
    st.metric(
        "Avg Processing Time",
        f"{avg_processing_time:.0f} sec"
    )

with k7:
    st.metric(
        "Critical Processing",
        f"{critical_processing:,}"
    )

with k8:
    st.metric(
        "Exceptions",
        f"{exceptions:,}"
    )


# ============================================================
# OPERATIONS HEALTH
# ============================================================

st.markdown(
    '<div class="section-heading">Operations Health</div>',
    unsafe_allow_html=True
)

st.caption(
    "Current indicators for transaction processing and reconciliation."
)

health_col, summary_col = st.columns(2)


with health_col:

    with st.container(border=True):

        st.markdown("#### Current Operational Health")

        st.write("Success Rate")
        st.progress(
            min(success_rate / 100, 1.0)
        )
        st.caption(
            f"{success_rate:.1f}%"
        )

        st.write("Reconciliation Rate")
        st.progress(
            min(reconciliation_rate / 100, 1.0)
        )
        st.caption(
            f"{reconciliation_rate:.1f}%"
        )

        st.write("Transactions Resolved")
        st.progress(
            min(
                reconciled_transactions / total_transactions,
                1.0
            ) if total_transactions else 0
        )
        st.caption(
            f"{reconciled_transactions:,} of "
            f"{total_transactions:,}"
        )


with summary_col:

    with st.container(border=True):

        st.markdown("#### Exception Summary")

        s1, s2, s3 = st.columns(3)

        with s1:
            st.metric(
                "Unreconciled",
                f"{unreconciled:,}"
            )

        with s2:
            st.metric(
                "Exceptions",
                f"{exceptions:,}"
            )

        with s3:
            st.metric(
                "Total Open Items",
                f"{unresolved_transactions:,}"
            )


# ============================================================
# STATUS ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-heading">Transaction & Reconciliation Status</div>',
    unsafe_allow_html=True
)

st.caption(
    "Break down transaction processing outcomes and reconciliation state."
)

col1, col2 = st.columns(2)


with col1:

    processing_counts = (
        filtered_df["processing_status"]
        .value_counts()
        .reset_index()
    )

    processing_counts.columns = [
        "Status",
        "Count"
    ]

    fig_processing = px.pie(
        processing_counts,
        names="Status",
        values="Count",
        hole=0.62
    )

    fig_processing.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111923",
        plot_bgcolor="#111923",
        margin=dict(
            l=20,
            r=20,
            t=45,
            b=20
        ),
        title="Processing Status"
    )

    st.plotly_chart(
        fig_processing,
        width="stretch"
    )


with col2:

    reconciliation_counts = (
        filtered_df["reconciliation_status"]
        .value_counts()
        .reset_index()
    )

    reconciliation_counts.columns = [
        "Status",
        "Count"
    ]

    fig_reconciliation = px.pie(
        reconciliation_counts,
        names="Status",
        values="Count",
        hole=0.62
    )

    fig_reconciliation.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111923",
        plot_bgcolor="#111923",
        margin=dict(
            l=20,
            r=20,
            t=45,
            b=20
        ),
        title="Reconciliation Status"
    )

    st.plotly_chart(
        fig_reconciliation,
        width="stretch"
    )


# ============================================================
# PAYMENT CHANNEL PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-heading">Payment Channel Performance</div>',
    unsafe_allow_html=True
)

st.caption(
    "Compare transaction success across payment channels."
)

channel_perf = (
    filtered_df
    .groupby("payment_channel")
    .agg(
        transactions=("transaction_id", "count"),
        successful=(
            "processing_status",
            lambda x: (x == "Successful").sum()
        )
    )
    .reset_index()
)

channel_perf["success_rate"] = (
    channel_perf["successful"]
    / channel_perf["transactions"]
    * 100
)

fig_channel = px.bar(
    channel_perf,
    x="payment_channel",
    y="success_rate",
    text="success_rate"
)

fig_channel.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_channel.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111923",
    plot_bgcolor="#111923",
    yaxis_title="Success Rate (%)",
    xaxis_title="Payment Channel",
    yaxis_range=[0, 100],
    margin=dict(
        l=30,
        r=30,
        t=25,
        b=30
    )
)

st.plotly_chart(
    fig_channel,
    width="stretch"
)


# ============================================================
# PROCESSING EFFICIENCY
# ============================================================

st.markdown(
    '<div class="section-heading">Processing Efficiency</div>',
    unsafe_allow_html=True
)

st.caption(
    "Average processing time by payment channel."
)

processing_efficiency = (
    filtered_df
    .groupby("payment_channel")
    ["processing_time_seconds"]
    .mean()
    .reset_index()
)

processing_efficiency.columns = [
    "payment_channel",
    "avg_processing_seconds"
]

fig_processing_time = px.bar(
    processing_efficiency,
    x="payment_channel",
    y="avg_processing_seconds",
    text="avg_processing_seconds"
)

fig_processing_time.update_traces(
    texttemplate="%{text:.0f}s",
    textposition="outside"
)

fig_processing_time.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111923",
    plot_bgcolor="#111923",
    yaxis_title="Average Processing Time (seconds)",
    xaxis_title="Payment Channel",
    margin=dict(
        l=30,
        r=30,
        t=25,
        b=30
    )
)

st.plotly_chart(
    fig_processing_time,
    width="stretch"
)


# ============================================================
# FAILURE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-heading">Failure Analysis</div>',
    unsafe_allow_html=True
)

st.caption(
    "Identify the most common transaction failure reasons."
)

failed_df = filtered_df[
    filtered_df["processing_status"] == "Failed"
].copy()

if len(failed_df) > 0:

    failure_counts = (
        failed_df["failure_reason"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    failure_counts.columns = [
        "failure_reason",
        "count"
    ]

    fig_failures = px.bar(
        failure_counts,
        x="count",
        y="failure_reason",
        orientation="h",
        text="count"
    )

    fig_failures.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111923",
        plot_bgcolor="#111923",
        xaxis_title="Failed Transactions",
        yaxis_title="Failure Reason",
        margin=dict(
            l=30,
            r=30,
            t=25,
            b=30
        )
    )

    st.plotly_chart(
        fig_failures,
        width="stretch"
    )

else:

    st.info(
        "No failed transactions match the selected filters."
    )


# ============================================================
# DAILY TRANSACTION VOLUME
# ============================================================

st.markdown(
    '<div class="section-heading">Transaction Volume Trend</div>',
    unsafe_allow_html=True
)

st.caption(
    "Daily transaction volume across the selected dataset."
)

daily_volume = (
    filtered_df
    .dropna(subset=["transaction_date"])
    .groupby(
        filtered_df["transaction_date"].dt.date
    )
    .size()
    .reset_index(name="transactions")
)

daily_volume.columns = [
    "date",
    "transactions"
]

fig_daily = px.line(
    daily_volume,
    x="date",
    y="transactions",
    markers=True
)

fig_daily.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111923",
    plot_bgcolor="#111923",
    xaxis_title="Date",
    yaxis_title="Transactions",
    margin=dict(
        l=30,
        r=30,
        t=25,
        b=30
    )
)

st.plotly_chart(
    fig_daily,
    width="stretch"
)


# ============================================================
# CURRENCY EXPOSURE
# ============================================================

st.markdown(
    '<div class="section-heading">Currency Exposure</div>',
    unsafe_allow_html=True
)

st.caption(
    "Transaction volume by currency. Monetary values remain separated by currency."
)

currency_counts = (
    filtered_df["currency"]
    .value_counts()
    .reset_index()
)

currency_counts.columns = [
    "currency",
    "transactions"
]

fig_currency = px.bar(
    currency_counts,
    x="currency",
    y="transactions",
    text="transactions"
)

fig_currency.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111923",
    plot_bgcolor="#111923",
    xaxis_title="Currency",
    yaxis_title="Transactions",
    margin=dict(
        l=30,
        r=30,
        t=25,
        b=30
    )
)

st.plotly_chart(
    fig_currency,
    width="stretch"
)


# ============================================================
# EXCEPTION MANAGEMENT
# ============================================================

st.markdown(
    '<div class="section-heading">Exception Management</div>',
    unsafe_allow_html=True
)

st.caption(
    "Review unresolved transactions requiring operational attention."
)

unresolved = filtered_df[
    filtered_df["reconciliation_status"]
    .isin(["Unreconciled", "Exception"])
].copy()


if len(unresolved) > 0:

    unresolved = unresolved.sort_values(
        "discrepancy_amount",
        ascending=False
    )

    display_columns = [
        "transaction_id",
        "transaction_date",
        "merchant_name",
        "payment_channel",
        "currency",
        "transaction_amount",
        "settled_amount",
        "discrepancy_amount",
        "reconciliation_status",
    ]

    display_columns = [
        col
        for col in display_columns
        if col in unresolved.columns
    ]

    display_df = unresolved[
        display_columns
    ].head(20).copy()

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )

else:

    st.success(
        "No unresolved transactions match the selected filters."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "NexaPay Operations Intelligence • "
    "Python • SQL • Streamlit • Plotly"
)
