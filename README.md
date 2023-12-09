# Solution 1: Loan Management System

# Overview
The SQL query extracts key information from a loan management system database, focusing on the latest details for each loan. The result includes the city, zip code, payment frequency, maturity date, days past due, last due date, last repayment date, and the amount at risk for each loan.

## SQL Query Explanation
The LoanDetails Common Table Expression (CTE) is created to organize and filter loan-related data.
The query selects relevant columns and uses various joins to gather information from different tables (Loan_table, Loan_payment, Payment_Schedule, and Borrower_table).
It calculates dynamic fields such as current_days_past_due, last_due_date, last_repayment_date, and amount_at_risk.
The ROW_NUMBER() function is applied to assign a row number to each record within the partition of each loan, ordered by the expected payment date in descending order.
The final query selects the latest details for each loan based on the row number and orders the results by city, zip code, and maturity date.

## Usage
To use this solution, execute the SQL query against the loan management system database. The query returns a result set with relevant loan details, focusing on the latest information for each loan.

NOTE: Postgresql is used as the sql server ide.

# Daily Currency Exchange Rate Updater

## Objective

The objective of this Python script and Apache Airflow DAG is to interact with the XE.com currency exchange rate API, extract daily exchange rates for seven countries, and update a PostgreSQL database with the latest rates. The script is designed to be modular, handling API connections, data extraction, and data loading, while the Airflow DAG orchestrates the execution on a daily schedule.

## Solution 2: Daily Currency Exchange Rate Updater with Apache Airflow

### Overview

This solution involves a Python script and an Apache Airflow DAG to automate the extraction of daily currency exchange rates and load them into a PostgreSQL database.

### Python Script Explanation

1. **Connect to XE.com API and Extract Daily Rates:**
   - The script includes a function (`connect_to_api_and_extract`) to create an instance for interacting with the XE.com API. It extracts daily rates for specified countries, creates dataframes, and returns a dictionary.

2. **Connect to PostgreSQL Database and Load Data:**
   - Another function (`connect_to_postgres_and_load_data`) in the script loads the extracted dataframes into specified tables in a PostgreSQL database using the PostgresHook.

3. **Airflow DAG Explanation:**
   - The Airflow DAG (`daily_extraction_of_currency_rates`) is defined with tasks for extracting data from the API (`extract_currency_data`) and loading it into PostgreSQL (`load_data_into_postgres`).
   - The DAG is scheduled to run daily at 1:00 AM and 11:00 PM.

### Usage

1. **Install Required Libraries:**
   - Open a terminal or command prompt.
   - Execute the following command to install the required Python libraries:

     ```bash
     pip install pandas xecd-rates-client sqlalchemy apache-airflow
     ```

2. **Set Environment Variables:**
   - Ensure you have the following environment variables set:
     - `ACCOUNT_ID`: Your XE.com account ID.
     - `API_KEY`: Your XE.com API key.
     - `POSTGRES_CONN_ID`: Specify the Airflow connection ID for PostgreSQL.

     ```bash
     export ACCOUNT_ID=your_account_id
     export API_KEY=your_api_key
     export POSTGRES_CONN_ID=your_postgres_conn_id
     ```

3. **Initialize Airflow Database:**
   - Run the following command to initialize the Airflow metadata database:

     ```bash
     airflow db init
     ```

4. **Start Airflow Scheduler and Web Server:**
   - Run the following commands to start the Airflow scheduler and web server:

     ```bash
     airflow scheduler
     ```

     In a separate terminal:

     ```bash
     airflow webserver
     ```

5. **Access Airflow Web UI:**
   - Open your web browser and access the Airflow Web UI at [http://localhost:8080](http://localhost:8080).
   - Enable the DAG (`daily_extraction_of_currency_rates`) from the Airflow Web UI.

6. **Review Output:**
   - The script will connect to the XE.com API, extract daily rates, and load them into your PostgreSQL database.
   - Check the Airflow Web UI for task execution logs and status.

**Note:** Ensure your PostgreSQL database is running and accessible before executing the script.
          The Api Key and Id was not exposed because its not best practice


