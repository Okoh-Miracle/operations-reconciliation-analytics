import pandas as pd

INPUT_FILE = "data/raw_transactions.csv"
OUTPUT_FILE = "data/clean_transactions.csv"

print("\n======================================")
print(" NexaPay Data Cleaning Pipeline")
print("======================================\n")

# 1. Load raw data
df = pd.read_csv(INPUT_FILE)

original_rows = len(df)

print(f"Raw rows loaded: {original_rows}")


# 2. Convert data types
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

numeric_columns = [
    "transaction_amount",
    "expected_amount",
    "settled_amount",
    "discrepancy_amount",
    "processing_time_seconds"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# 3. Remove duplicate transactions
duplicate_count = df.duplicated(
    subset="transaction_id"
).sum()

df = df.drop_duplicates(
    subset="transaction_id",
    keep="first"
)

print(
    f"Duplicate transaction records removed: "
    f"{duplicate_count}"
)


# 4. Handle missing merchant IDs
missing_merchant_ids = df["merchant_id"].isna().sum()

df["merchant_id"] = df["merchant_id"].fillna(
    "UNKNOWN"
)

print(
    f"Missing merchant IDs handled: "
    f"{missing_merchant_ids}"
)


# 5. Handle missing processing times
missing_processing_times = (
    df["processing_time_seconds"].isna().sum()
)

median_processing_time = (
    df["processing_time_seconds"].median()
)

df["processing_time_seconds"] = (
    df["processing_time_seconds"].fillna(
        median_processing_time
    )
)

print(
    f"Missing processing times handled: "
    f"{missing_processing_times}"
)

print(
    f"Median processing time used: "
    f"{median_processing_time:.2f} seconds"
)


# 6. Standardize failure reasons
df["failure_reason"] = df[
    "failure_reason"
].fillna("Not Applicable")


# 7. Validate monetary values
negative_amounts = (
    df["transaction_amount"] < 0
).sum()

negative_settlements = (
    df["settled_amount"] < 0
).sum()

print(
    f"Negative transaction amounts: "
    f"{negative_amounts}"
)

print(
    f"Negative settlement amounts: "
    f"{negative_settlements}"
)


# 8. Recalculate discrepancy
df["discrepancy_amount"] = (
    df["expected_amount"]
    - df["settled_amount"]
).round(2)


# 9. Create processing-time category
def classify_processing_time(seconds):

    if seconds <= 60:
        return "Fast"

    elif seconds <= 300:
        return "Normal"

    elif seconds <= 900:
        return "Slow"

    else:
        return "Critical"


df["processing_time_category"] = (
    df["processing_time_seconds"]
    .apply(classify_processing_time)
)


# 10. Final quality checks
remaining_duplicates = df.duplicated(
    subset="transaction_id"
).sum()

remaining_missing_merchant_ids = (
    df["merchant_id"].isna().sum()
)

remaining_missing_processing_times = (
    df["processing_time_seconds"].isna().sum()
)


# 11. Save cleaned dataset
df.to_csv(
    OUTPUT_FILE,
    index=False
)


# 12. Cleaning summary
print("\n======================================")
print(" Cleaning Summary")
print("======================================")

print(f"\nOriginal rows: {original_rows}")

print(f"Clean rows: {len(df)}")

print(
    f"Rows removed: "
    f"{original_rows - len(df)}"
)

print(
    f"Remaining duplicate IDs: "
    f"{remaining_duplicates}"
)

print(
    f"Remaining missing merchant IDs: "
    f"{remaining_missing_merchant_ids}"
)

print(
    f"Remaining missing processing times: "
    f"{remaining_missing_processing_times}"
)

print(
    f"\nClean dataset saved to:"
    f"\n{OUTPUT_FILE}"
)

print("\n======================================")
print(" Data Cleaning Complete")
print("======================================\n")
