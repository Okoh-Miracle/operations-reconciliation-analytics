import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# -----------------------------
# CONFIGURATION
# -----------------------------

NUM_TRANSACTIONS = 1000

payment_channels = [
    "Card",
    "Bank Transfer",
    "Mobile Money",
    "USSD",
    "Wallet"
]

currencies = ["NGN", "USD", "GBP", "EUR"]

processing_statuses = [
    "Successful",
    "Successful",
    "Successful",
    "Successful",
    "Failed",
    "Pending"
]

failure_reasons = [
    "Insufficient Funds",
    "Network Timeout",
    "Bank Declined",
    "Invalid Account",
    "Fraud Check",
    "System Error",
    "None"
]

merchants = [
    ["MER-001", "SwiftMart", "Retail"],
    ["MER-002", "Apex Travel", "Travel"],
    ["MER-003", "Nova Health", "Healthcare"],
    ["MER-004", "Urban Eats", "Food"],
    ["MER-005", "Prime Electronics", "Electronics"],
    ["MER-006", "Green Energy", "Energy"],
    ["MER-007", "Metro Logistics", "Logistics"],
    ["MER-008", "CloudLearn", "Education"],
    ["MER-009", "StyleHouse", "Fashion"],
    ["MER-010", "Global Services", "Professional Services"],
]

# -----------------------------
# GENERATE TRANSACTIONS
# -----------------------------

start_date = datetime(2026, 1, 1)

transactions = []

for i in range(1, NUM_TRANSACTIONS + 1):

    transaction_id = f"TXN-{i:05d}"

    transaction_date = start_date + timedelta(
        minutes=random.randint(0, 260000)
    )

    merchant = random.choice(merchants)

    merchant_id = merchant[0]
    merchant_name = merchant[1]

    payment_channel = random.choice(payment_channels)

    currency = random.choice(currencies)

    amount = round(random.uniform(100, 250000), 2)

    processing_status = random.choice(processing_statuses)

    processing_time = random.randint(1, 900)

    if processing_status == "Successful":

        settlement_status = random.choices(
            ["Settled", "Settlement Exception"],
            weights=[96, 4]
        )[0]

    elif processing_status == "Failed":

        settlement_status = "Not Settled"

    else:

        settlement_status = random.choice(
            ["Pending", "Not Settled"]
        )

    if settlement_status == "Settled":

        # Normally settled amount equals expected amount
        settled_amount = amount

        # Occasionally introduce a discrepancy
        if random.random() < 0.04:

            difference = round(
                random.uniform(10, 5000), 2
            )

            settled_amount = round(
                amount - difference, 2
            )

    else:

        settled_amount = 0

    discrepancy_amount = round(
        amount - settled_amount, 2
    )

    if processing_status == "Failed":

        failure_reason = random.choice(
            failure_reasons[:-1]
        )

    elif processing_status == "Pending":

        failure_reason = "Pending Review"

    else:

        failure_reason = "None"

    if discrepancy_amount == 0 and settlement_status == "Settled":

        reconciliation_status = "Reconciled"

    elif settlement_status == "Not Settled":

        reconciliation_status = "Unreconciled"

    elif discrepancy_amount != 0:

        reconciliation_status = "Exception"

    else:

        reconciliation_status = "Pending"

    transactions.append([
        transaction_id,
        transaction_date,
        merchant_id,
        merchant_name,
        payment_channel,
        currency,
        amount,
        processing_status,
        settlement_status,
        reconciliation_status,
        amount,
        settled_amount,
        discrepancy_amount,
        failure_reason,
        processing_time
    ])


# -----------------------------
# CREATE DATAFRAME
# -----------------------------

columns = [
    "transaction_id",
    "transaction_date",
    "merchant_id",
    "merchant_name",
    "payment_channel",
    "currency",
    "transaction_amount",
    "processing_status",
    "settlement_status",
    "reconciliation_status",
    "expected_amount",
    "settled_amount",
    "discrepancy_amount",
    "failure_reason",
    "processing_time_seconds"
]

df = pd.DataFrame(
    transactions,
    columns=columns
)


# -----------------------------
# INTRODUCE REALISTIC DATA ISSUES
# -----------------------------

# 1. Duplicate a few transactions
duplicates = df.sample(
    8,
    random_state=42
)

df = pd.concat(
    [df, duplicates],
    ignore_index=True
)

# 2. Missing merchant IDs
missing_indices = df.sample(
    12,
    random_state=10
).index

df.loc[
    missing_indices,
    "merchant_id"
] = None

# 3. Missing processing times
missing_time_indices = df.sample(
    10,
    random_state=20
).index

df.loc[
    missing_time_indices,
    "processing_time_seconds"
] = None

# 4. A few suspiciously high processing times
slow_indices = df.sample(
    15,
    random_state=30
).index

df.loc[
    slow_indices,
    "processing_time_seconds"
] = random.choices(
    range(1200, 3600),
    k=len(slow_indices)
)

# 5. Shuffle the data
df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


# -----------------------------
# SAVE RAW DATA
# -----------------------------

df.to_csv(
    "data/raw_transactions.csv",
    index=False
)

# Supporting merchant table
merchant_df = pd.DataFrame(
    merchants,
    columns=[
        "merchant_id",
        "merchant_name",
        "industry"
    ]
)

merchant_df.to_csv(
    "data/merchants.csv",
    index=False
)

# Payment channel reference table
channel_df = pd.DataFrame({
    "channel_id": [
        "CH-001",
        "CH-002",
        "CH-003",
        "CH-004",
        "CH-005"
    ],
    "payment_channel": payment_channels,
    "channel_type": [
        "Digital Card",
        "Banking",
        "Mobile",
        "USSD",
        "Digital Wallet"
    ]
})

channel_df.to_csv(
    "data/payment_channels.csv",
    index=False
)


# -----------------------------
# SUMMARY
# -----------------------------

print()
print("======================================")
print(" NexaPay Dataset Generated")
print("======================================")
print()
print(f"Transaction rows: {len(df)}")
print(f"Unique transaction IDs: {df['transaction_id'].nunique()}")
print()
print("Files created:")
print(" - data/raw_transactions.csv")
print(" - data/merchants.csv")
print(" - data/payment_channels.csv")
print()
print("Processing status:")
print(df["processing_status"].value_counts())
print()
print("Reconciliation status:")
print(df["reconciliation_status"].value_counts())
print()
print("Dataset generation complete.")
