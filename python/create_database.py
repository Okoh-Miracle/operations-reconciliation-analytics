import pandas as pd
import sqlite3
import os

# ======================================
# NEXAPAY DATABASE CREATION
# ======================================

DATABASE_FILE = "data/nexapay.db"

TRANSACTIONS_FILE = "data/clean_transactions.csv"
MERCHANTS_FILE = "data/merchants.csv"
CHANNELS_FILE = "data/payment_channels.csv"

print("\n======================================")
print(" NexaPay SQLite Database Setup")
print("======================================\n")


# ======================================
# 1. LOAD CSV FILES
# ======================================

transactions = pd.read_csv(
    TRANSACTIONS_FILE
)

merchants = pd.read_csv(
    MERCHANTS_FILE
)

payment_channels = pd.read_csv(
    CHANNELS_FILE
)

print(
    f"Transactions loaded: "
    f"{len(transactions)}"
)

print(
    f"Merchants loaded: "
    f"{len(merchants)}"
)

print(
    f"Payment channels loaded: "
    f"{len(payment_channels)}"
)


# ======================================
# 2. CREATE SQLITE DATABASE
# ======================================

# Remove existing database if present
if os.path.exists(DATABASE_FILE):
    os.remove(DATABASE_FILE)

conn = sqlite3.connect(
    DATABASE_FILE
)


# ======================================
# 3. CREATE TABLES
# ======================================

transactions.to_sql(
    "transactions",
    conn,
    if_exists="replace",
    index=False
)

merchants.to_sql(
    "merchants",
    conn,
    if_exists="replace",
    index=False
)

payment_channels.to_sql(
    "payment_channels",
    conn,
    if_exists="replace",
    index=False
)


# ======================================
# 4. VERIFY TABLES
# ======================================

tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
    """,
    conn
)

print("\nDATABASE TABLES")
print("--------------------------------------")

print(
    tables.to_string(index=False)
)


# ======================================
# 5. VERIFY ROW COUNTS
# ======================================

print("\nROW COUNTS")
print("--------------------------------------")

for table in [
    "transactions",
    "merchants",
    "payment_channels"
]:

    result = pd.read_sql_query(
        f"SELECT COUNT(*) AS row_count FROM {table}",
        conn
    )

    print(
        f"{table}: "
        f"{result.iloc[0]['row_count']}"
    )


# ======================================
# 6. CLOSE CONNECTION
# ======================================

conn.close()


# ======================================
# COMPLETE
# ======================================

print("\n======================================")
print(" Database Creation Complete")
print("======================================")

print(
    f"\nDatabase created at:"
    f"\n{DATABASE_FILE}"
)

print()
