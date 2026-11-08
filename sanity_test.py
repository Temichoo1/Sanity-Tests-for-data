import pandas as pd

import pytest

FILE_PATH = r"data\customers-100.csv"
# ==========================
# FILE VALIDATION TESTS
# ==========================

def test_file_not_empty():
    """
    Verify the source file contains data.
    """
    data_df = pd.read_csv(r"data\customers-100.csv")

    assert not data_df.empty, (
        "Source file is empty. Please check the ETL process."
    )


def test_expected_columns_exist():
    """
    Verify required columns exist.
    """
    data_df = pd.read_csv(r"data\customers-100.csv")

    expected_columns = [
    "Index",
    "CustomerId",
    "First Name",
    "Last Name",
    "Company",
    "City",
    "Country",
    "Phone 1",
    "Phone 2",
    "Email",
    "Subscription Date",
    "Website",
    "Amount",
    "Age"
]

    missing_columns = [
        col for col in expected_columns
        if col not in data_df.columns
    ]

    assert len(missing_columns) == 0, (
        f"Missing columns: {missing_columns}"
    )


# ==========================
# DUPLICATE TESTS
# ==========================

def test_no_duplicate_rows():
    """
    Check for duplicate records.
    """
    data_df = pd.read_csv(r"data\customers-100.csv")

    duplicate_count = data_df.duplicated().sum()

    assert duplicate_count == 0, (
        f"{duplicate_count} duplicate records found."
    )


def test_customerid_unique():
    """
    Check CustomerId is unique.
    """
    data_df = pd.read_csv(r"data\customers-100.csv")

    duplicate_customerids = (
        data_df["CustomerId"]
        .duplicated()
        .sum()
    )

    assert duplicate_customerids == 0, (
        f"{duplicate_customerids} duplicate CustomerIds found."
    )


# ==========================
# NULL TESTS
# ==========================

def test_customerid_not_null():
    data_df = pd.read_csv(r"data\customers-100.csv")

    null_count = data_df["CustomerId"].isna().sum()

    assert null_count == 0, (
        f"CustomerId contains {null_count} null values."
    )


def test_email_not_null():
    data_df = pd.read_csv(r"data\customers-100.csv")

    null_count = data_df["Email"].isna().sum()

    assert null_count == 0, (
        f"Email contains {null_count} null values."
    )


# ==========================
# DATA TYPE TESTS
# ==========================

def test_customerid_numeric():
    data_df = pd.read_csv(r"data\customers-100.csv")

    invalid_count = pd.to_numeric(
        data_df["CustomerId"],
        errors="coerce"
    ).isna().sum()

    assert invalid_count == 0, (
        f"{invalid_count} invalid CustomerIds found."
    )


# ==========================
# DATE VALIDATION
# ==========================

def test_valid_order_date():
    data_df = pd.read_csv(r"data\customers-100.csv")

    invalid_dates = pd.to_datetime(
        data_df["Subscription Date"],
        errors="coerce"
    ).isna().sum()

    assert invalid_dates == 0, (
        f"{invalid_dates} invalid dates found."
    )


# ==========================
# VALUE RANGE TESTS
# ==========================

def test_amount_positive():
    data_df = pd.read_csv(r"data\customers-100.csv")

    invalid_amounts = (
        data_df["Amount"] <= 0
    ).sum()

    assert invalid_amounts == 0, (
        f"{invalid_amounts} records have invalid Amount values."
    )


def test_customer_age_valid():
    data_df = pd.read_csv(r"data\customers-100.csv")

    invalid_age_count = (
        (data_df["Age"] < 18) |
        (data_df["Age"] > 120)
    ).sum()

    assert invalid_age_count == 0, (
        f"{invalid_age_count} invalid ages found."
    )


# ==========================
# EMAIL VALIDATION
# ==========================

def test_email_format():
    data_df = pd.read_csv(r"data\customers-100.csv")

    invalid_emails = (
        ~data_df["Email"]
        .astype(str)
        .str.contains(
            r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            regex=True,
            na=False
        )
    ).sum()

    assert invalid_emails == 0, (
        f"{invalid_emails} invalid email addresses found."
    )


# ==========================
# BUSINESS RULE TESTS
# ==========================

def test_sales_greater_than_zero():
    data_df = pd.read_csv(r"data\customers-100.csv")

    invalid_sales = (
        data_df["Sales"] <= 0
    ).sum()

    assert invalid_sales == 0, (
        f"{invalid_sales} records contain invalid sales values."
    )


def test_row_count_above_threshold():
    data_df = pd.read_csv(r"data\customers-100.csv")

    minimum_rows = 100

    assert len(data_df) >= minimum_rows, (
        f"Expected at least {minimum_rows} rows. "
        f"Found {len(data_df)}."
    )