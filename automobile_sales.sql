WITH LoanDetails AS (
    SELECT
	    lp.LOAN_ID,
        b.City,
        b.zip_code,
        l.Payment_frequency,
        l.Maturity_date,
	    (CURRENT_DATE - ps.Expected_payment_date) AS current_days_past_due,
        MAX(ps.Expected_payment_date) AS last_due_date,
        MAX(lp.Date_paid) AS last_repayment_date,
	    --lp.Date_paid AS last_repayment_date,
        (SUM(ps.Expected_payment_amount)) - (SUM(lp.Amount_paid)) AS amount_at_risk,
	ROW_NUMBER() OVER (PARTITION BY lp.LOAN_ID ORDER BY ps.Expected_payment_date DESC) AS row_num
    FROM Loan_table l 
	LEFT JOIN Loan_payment lp ON l.loan_id = lp.loan_id
	LEFT JOIN Payment_Schedule ps ON l.Loan_id = ps.Loan_id
    LEFT JOIN Borrower_table b ON l.Borrower_id = b.Borrower_id
    GROUP BY lp.LOAN_ID, b.City, b.zip_code, l.Payment_frequency, l.Maturity_date,
	PS.Expected_payment_date
)

SELECT
    City,
    zip_code,
    Payment_frequency,
    Maturity_date,
    current_days_past_due,
    last_due_date,
	last_repayment_date,
    --CASE WHEN last_repayment_date IS NULL THEN 'N/A' ELSE last_repayment_date::TEXT END AS last_repayment_date
    amount_at_risk
FROM LoanDetails
WHERE row_num = 1
ORDER BY City, zip_code, Maturity_date;
