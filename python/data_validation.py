import pandas as pd

INPUT_FILE = "data/clean_transactions.csv"

print("\n======================================")
print(" NexaPay Data Validation Report")
print("======================================\n")


# ======================================
# 1. LOAD CLEAN DATA
# ======================================

df = pd.read_csv(INPUT_FILE)

print(f"Rows loaded: {len(df)}")


# ======================================
# 2. VALIDATION RESULTS
# ======================================

validation_results = []


# ======================================
# RULE 1: TRANSACTION IDs MUST BE UNIQUE
# ======================================

duplicate_ids = df["transaction_id"].duplicated().sum()

validation_results.append({
    "check": "Unique transaction IDs",
    "status": "PASS" if duplicate_ids == 0 else "FAIL",
    "issues": duplicate_ids
})


# ======================================
# RULE 2: TRANSACTION AMOUNTS
# MUST NOT BE NEGATIVE
# ======================================

negative_transactions = (
    df["transaction_amount"] < 0
).sum()

validation_results.append({
    "check": "Non-negative transaction amounts",
    "status": (
        "PASS"
        if negative_transactions == 0
        else "FAIL"
    ),
    "issues": negative_transactions
})


# ======================================
# RULE 3: SETTLED AMOUNT
# MUST NOT BE NEGATIVE
# ======================================

negative_settlements = (
    df["settled_amount"] < 0
).sum()

validation_results.append({
    "check": "Non-negative settlement amounts",
    "status": (
        "PASS"
        if negative_settlements == 0
        else "FAIL"
    ),
    "issues": negative_settlements
})


# ======================================
# RULE 4: DISCREPANCY MUST MATCH
# EXPECTED - SETTLED
# ======================================

expected_discrepancy = (
    df["expected_amount"]
    - df["settled_amount"]
).round(2)

discrepancy_errors = (
    df["discrepancy_amount"]
    != expected_discrepancy
).sum()

validation_results.append({
    "check": "Discrepancy calculation",
    "status": (
        "PASS"
        if discrepancy_errors == 0
        else "FAIL"
    ),
    "issues": discrepancy_errors
})


# ======================================
# RULE 5: RECONCILED TRANSACTIONS
# MUST HAVE ZERO DISCREPANCY
# ======================================

invalid_reconciled = (
    (df["reconciliation_status"] == "Reconciled")
    & (df["discrepancy_amount"] != 0)
).sum()

validation_results.append({
    "check": "Reconciled transactions have zero discrepancy",
    "status": (
        "PASS"
        if invalid_reconciled == 0
        else "FAIL"
    ),
    "issues": invalid_reconciled
})


# ======================================
# RULE 6: FAILED TRANSACTIONS
# SHOULD NOT BE SETTLED
# ======================================

invalid_failed_settlements = (
    (df["processing_status"] == "Failed")
    & (df["settlement_status"] == "Settled")
).sum()

validation_results.append({
    "check": "Failed transactions are not settled",
    "status": (
        "PASS"
        if invalid_failed_settlements == 0
        else "FAIL"
    ),
    "issues": invalid_failed_settlements
})


# ======================================
# RULE 7: PROCESSING TIME
# MUST NOT BE NEGATIVE
# ======================================

negative_processing_times = (
    df["processing_time_seconds"] < 0
).sum()

validation_results.append({
    "check": "Non-negative processing times",
    "status": (
        "PASS"
        if negative_processing_times == 0
        else "FAIL"
    ),
    "issues": negative_processing_times
})


# ======================================
# RULE 8: REQUIRED FIELDS
# ======================================

required_columns = [
    "transaction_id",
    "transaction_date",
    "merchant_id",
    "payment_channel",
    "transaction_amount",
    "processing_status",
    "settlement_status",
    "reconciliation_status"
]

missing_required_values = (
    df[required_columns]
    .isnull()
    .sum()
    .sum()
)

validation_results.append({
    "check": "Required fields populated",
    "status": (
        "PASS"
        if missing_required_values == 0
        else "FAIL"
    ),
    "issues": missing_required_values
})


# ======================================
# CREATE VALIDATION DATAFRAME
# ======================================

results_df = pd.DataFrame(
    validation_results
)


# ======================================
# DISPLAY RESULTS
# ======================================

print("\nVALIDATION RESULTS")
print("--------------------------------------")

print(
    results_df.to_string(
        index=False
    )
)


# ======================================
# SUMMARY
# ======================================

passed = (
    results_df["status"] == "PASS"
).sum()

failed = (
    results_df["status"] == "FAIL"
).sum()

print("\n======================================")
print(" Validation Summary")
print("======================================")

print(f"Checks passed: {passed}")
print(f"Checks failed: {failed}")

if failed == 0:
    print("\nOverall result: PASS")
else:
    print("\nOverall result: REVIEW REQUIRED")

print("\n======================================")
print(" Data Validation Complete")
print("======================================\n")
