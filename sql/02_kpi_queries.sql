-- ============================================
-- NEXAPAY OPERATIONAL KPI QUERIES
-- ============================================

-- 1. TOTAL TRANSACTIONS
SELECT
    COUNT(*) AS total_transactions
FROM transactions;


-- 2. PROCESSING STATUS
SELECT
    processing_status,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY processing_status
ORDER BY transaction_count DESC;


-- 3. SUCCESS RATE
SELECT
    ROUND(
        SUM(
            CASE
                WHEN processing_status = 'Successful'
                THEN 1 ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS success_rate_percent
FROM transactions;


-- 4. RECONCILIATION RATE
SELECT
    ROUND(
        SUM(
            CASE
                WHEN reconciliation_status = 'Reconciled'
                THEN 1 ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS reconciliation_rate_percent
FROM transactions;


-- 5. RECONCILIATION STATUS
SELECT
    reconciliation_status,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY reconciliation_status
ORDER BY transaction_count DESC;


-- 6. UNRESOLVED TRANSACTIONS
SELECT
    COUNT(*) AS unresolved_transactions
FROM transactions
WHERE reconciliation_status IN ('Unreconciled', 'Exception');


-- 7. AVERAGE PROCESSING TIME
SELECT
    ROUND(AVG(processing_time_seconds), 2)
        AS average_processing_seconds
FROM transactions;


-- 8. CRITICAL PROCESSING TRANSACTIONS
SELECT
    COUNT(*) AS critical_processing_transactions
FROM transactions
WHERE processing_time_category = 'Critical';


-- 9. TOP FAILURE REASON
SELECT
    failure_reason,
    COUNT(*) AS failure_count
FROM transactions
WHERE processing_status = 'Failed'
GROUP BY failure_reason
ORDER BY failure_count DESC
LIMIT 1;


-- 10. PAYMENT CHANNEL PERFORMANCE
SELECT
    payment_channel,
    COUNT(*) AS transaction_count,
    ROUND(
        SUM(
            CASE
                WHEN processing_status = 'Successful'
                THEN 1 ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS success_rate_percent,
    ROUND(AVG(processing_time_seconds), 2)
        AS average_processing_seconds
FROM transactions
GROUP BY payment_channel
ORDER BY success_rate_percent DESC;


-- 11. DAILY TRANSACTION VOLUME
SELECT
    DATE(transaction_date) AS transaction_day,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY DATE(transaction_date)
ORDER BY transaction_day;


-- 12. LARGEST UNRESOLVED TRANSACTIONS
SELECT
    transaction_id,
    merchant_id,
    payment_channel,
    currency,
    transaction_amount,
    discrepancy_amount,
    reconciliation_status
FROM transactions
WHERE reconciliation_status IN ('Unreconciled', 'Exception')
ORDER BY transaction_amount DESC
LIMIT 10;
