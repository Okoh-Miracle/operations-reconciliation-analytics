# NexaPay Operations Reconciliation Dashboard

## Dashboard Purpose

The dashboard provides an operational view of transaction processing,
reconciliation performance, payment-channel performance, and unresolved
transaction exceptions.

## Primary Users

- Payments Operations Managers
- Reconciliation Analysts
- Finance Operations Teams
- Technical Operations Teams

## KPI Cards

The dashboard should display:

1. Total Transactions
2. Successful Transactions
3. Success Rate
4. Reconciliation Rate
5. Unresolved Transactions
6. Average Processing Time
7. Critical Processing Transactions

## Visual 1 — Transaction Processing Status

Chart type:
Donut chart

Dimension:
Processing Status

Values:
Transaction Count

Categories:
- Successful
- Pending
- Failed

Purpose:
Show the overall distribution of transaction processing outcomes.

## Visual 2 — Reconciliation Status

Chart type:
Donut chart

Dimension:
Reconciliation Status

Values:
Transaction Count

Categories:
- Reconciled
- Unreconciled
- Exception

Purpose:
Show the current reconciliation workload and unresolved transaction volume.

## Visual 3 — Payment Channel Performance

Chart type:
Clustered bar chart

Dimension:
Payment Channel

Metrics:
- Transaction Count
- Success Rate

Purpose:
Compare operational performance across payment channels.

## Visual 4 — Average Processing Time by Channel

Chart type:
Bar chart

Dimension:
Payment Channel

Metric:
Average Processing Time

Purpose:
Identify channels with slower transaction processing.

## Visual 5 — Daily Transaction Volume

Chart type:
Line chart

X-axis:
Transaction Date

Y-axis:
Transaction Count

Purpose:
Monitor transaction activity over time and identify unusual volume patterns.

## Visual 6 — Failure Reasons

Chart type:
Horizontal bar chart

Dimension:
Failure Reason

Metric:
Failure Count

Purpose:
Identify the most common causes of failed transactions.

## Visual 7 — Exceptions by Payment Channel

Chart type:
Bar chart

Dimension:
Payment Channel

Metric:
Exception Count

Purpose:
Identify payment channels generating the largest reconciliation workload.

## Visual 8 — Currency Exposure

Chart type:
Column chart

Dimension:
Currency

Metric:
Transaction Count

Purpose:
Show transaction distribution across the supported currencies.

## Detail Table — High-Value Unresolved Transactions

Columns:

- Transaction ID
- Transaction Date
- Merchant
- Payment Channel
- Currency
- Transaction Amount
- Settled Amount
- Discrepancy Amount
- Reconciliation Status

Purpose:
Give operations analysts a practical exception-management queue.

## Suggested Dashboard Layout

### Top Row
KPI cards

### Second Row
Transaction Processing Status
Reconciliation Status

### Third Row
Payment Channel Performance
Average Processing Time by Channel

### Fourth Row
Daily Transaction Volume
Failure Reasons

### Fifth Row
Exceptions by Payment Channel
Currency Exposure

### Bottom
High-Value Unresolved Transactions table

## Operational Questions Answered

The dashboard should allow an operations team to answer:

- How many transactions were processed?
- What percentage succeeded?
- How many transactions remain unresolved?
- Which payment channels have lower success rates?
- Which channels take longer to process?
- What are the most common failure reasons?
- How does transaction volume change over time?
- Which transactions require investigation?
- Which currencies are represented in the transaction population?
