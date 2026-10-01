-- ============================================
-- NEXAPAY RECONCILIATION ANALYSIS
-- ============================================


-- ============================================
-- 1. OVERALL TRANSACTION SUMMARY
-- ============================================

SELECT
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT transaction_id) AS unique_transactions,
    SUM(transaction_amount) AS total_transaction_value,
    AVG(transaction_amount) AS average_transaction_value
FROM transactions;


-- ============================================
-- 2. PROCESSING STATUS SUMMARY
-- ============================================

SELECT
    processing_status,
    COUNT(*) AS transaction_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM transactions),
        2
    ) AS percentage_of_transactions
FROM transactions
GROUP BY processing_status
ORDER BY transaction_count DESC;


-- ============================================
-- 3. RECONCILIATION STATUS
-- ============================================

SELECT
    reconciliation_status,
    COUNT(*) AS transaction_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM transactions),
        2
    ) AS percentage_of_transactions,
    SUM(discrepancy_amount) AS discrepancy_value
FROM transactions
GROUP BY reconciliation_status
ORDER BY transaction_count DESC;


-- ============================================
-- 4. PAYMENT CHANNEL PERFORMANCE
-- ============================================

SELECT
    payment_channel,
    COUNT(*) AS total_transactions,

    SUM(
        CASE
            WHEN processing_status = 'Successful'
            THEN 1
            ELSE 0
        END
    ) AS successful_transactions,

    SUM(
        CASE
            WHEN processing_status = 'Failed'
            THEN 1
            ELSE 0
        END
    ) AS failed_transactions,

    ROUND(
        SUM(
            CASE
                WHEN processing_status = 'Successful'
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS success_rate,

    ROUND(
        AVG(processing_time_seconds),
        2
    ) AS average_processing_seconds

FROM transactions

GROUP BY payment_channel

ORDER BY success_rate DESC;


-- ============================================
-- 5. FAILURE REASONS
-- ============================================

SELECT
    failure_reason,
    COUNT(*) AS failure_count
FROM transactions
WHERE processing_status = 'Failed'
GROUP BY failure_reason
ORDER BY failure_count DESC;


-- ============================================
-- 6. DISCREPANCIES BY PAYMENT CHANNEL
-- ============================================

SELECT
    payment_channel,
    COUNT(*) AS exception_count,
    ROUND(
        SUM(discrepancy_amount),
        2
    ) AS total_discrepancy,
    ROUND(
        AVG(discrepancy_amount),
        2
    ) AS average_discrepancy
FROM transactions
WHERE discrepancy_amount > 0
GROUP BY payment_channel
ORDER BY total_discrepancy DESC;


-- ============================================
-- 7. MERCHANT PERFORMANCE
-- ============================================

SELECT
    t.merchant_id,
    m.merchant_name,
    m.industry,

    COUNT(t.transaction_id)
        AS transaction_count,

    ROUND(
        SUM(t.transaction_amount),
        2
    ) AS transaction_value,

    SUM(
        CASE
            WHEN t.reconciliation_status
                 IN ('Unreconciled', 'Exception')
            THEN 1
            ELSE 0
        END
    ) AS unresolved_transactions

FROM transactions t

LEFT JOIN merchants m
    ON t.merchant_id = m.merchant_id

GROUP BY
    t.merchant_id,
    m.merchant_name,
    m.industry

ORDER BY unresolved_transactions DESC;


-- ============================================
-- 8. HIGH-VALUE UNRECONCILED TRANSACTIONS
-- ============================================

SELECT
    transaction_id,
    transaction_date,
    merchant_name,
    payment_channel,
    currency,
    transaction_amount,
    settled_amount,
    discrepancy_amount,
    reconciliation_status
FROM transactions
WHERE reconciliation_status
    IN ('Unreconciled', 'Exception')
ORDER BY transaction_amount DESC
LIMIT 20;
