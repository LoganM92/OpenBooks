import MySQLdb
import os
from datetime import datetime
import csv
import webbrowser
from fpdf import FPDF

# Database connection details  
DB_HOST = "localhost"
DB_USER = "root"  
DB_PASSWORD = "password"  
DB_NAME = "my_new_database"  


# Connect to the database
def connect_to_db():
    try:
        return MySQLdb.connect(
            host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME
        )
    except MySQLdb.Error as e:
        print(f"Error connecting to database: {e}")
        return None  # Or handle the error as needed


# Fetch balance sheet data - 
def fetch_balance_sheet_data(balance_date=None):  # Accepts optional balance_date
    conn = connect_to_db()
    if not conn:
        return None

    cursor = conn.cursor()

    try:
        if balance_date:  # Filter by balance_date if provided
            query = """
                SELECT coa.account_name, coa.account_type, ab.openbooks_balance, ab.bank_balance
                FROM AccountBalances ab
                JOIN ChartOfAccounts coa ON ab.chart_of_accounts_id = coa.id
                WHERE ab.balance_date = %s; 
            """
            cursor.execute(query, (balance_date,))
        else:  # Get the most recent balance for each account if no date is provided
            query = """
            SELECT coa.account_name, coa.account_type, ab.openbooks_balance, ab.bank_balance
            FROM AccountBalances ab
            JOIN ChartOfAccounts coa ON ab.chart_of_accounts_id = coa.id
            WHERE ab.balance_date = (SELECT MAX(balance_date) FROM AccountBalances);
            """
            cursor.execute(query)

        account_balances = cursor.fetchall()
        cursor.close()
        conn.close()

        balance_sheet_data = {}
        for account_name, account_type, openbooks_balance, bank_balance in account_balances:
            total_balance = (openbooks_balance or 0) + (bank_balance or 0)
            if account_type not in balance_sheet_data:
                balance_sheet_data[account_type] = {}
            balance_sheet_data[account_type][account_name] = total_balance

        return balance_sheet_data

    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None


def generate_balance_sheet_pdf(balance_sheet_data, filename="balance_sheet.pdf"):
    """Generates a PDF file to display the balance sheet."""

    pdf = FPDF()
    pdf.add_page()

    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S UTC")
    pdf.set_font("Arial", "B", size=16)  # Bold and larger title
    pdf.cell(200, 10, txt=f"Balance Sheet - {date_string}", ln=1, align="C")

    pdf.set_font("Arial", size=12)  # Set default font

    asset_accounts = balance_sheet_data.get("Asset", {})
    liability_accounts = balance_sheet_data.get("Liability", {})
    equity_accounts = balance_sheet_data.get("Equity", {})

    def add_account_section(accounts, section_title):
        if accounts:
            pdf.set_font("Arial", "B", size=12)  # Bold section title
            pdf.cell(200, 10, txt=section_title, ln=1, align="L")

            pdf.set_font("Arial", size=12)  # Regular font for account details
            for account_name, amount in accounts.items():
                pdf.cell(100, 10, txt=account_name, ln=0, align="L")
                pdf.cell(100, 10, txt=f"${amount:,.2f}", ln=1, align="R")

    add_account_section(asset_accounts, "ASSETS")
    total_assets = sum(asset_accounts.values()) if asset_accounts else 0
    if total_assets > 0:
        pdf.set_font("Arial", "B", size=12)  # Bold total
        pdf.cell(100, 10, txt="Total Assets", ln=0, align="L")
        pdf.cell(100, 10, txt=f"${total_assets:,.2f}", ln=1, align="R")
        pdf.set_font("Arial", size=12)

    add_account_section(liability_accounts, "LIABILITIES")
    total_liabilities = sum(liability_accounts.values()) if liability_accounts else 0
    if total_liabilities > 0:
        pdf.set_font("Arial", "B", size=12)  # Bold total
        pdf.cell(100, 10, txt="Total Liabilities", ln=0, align="L")
        pdf.cell(100, 10, txt=f"${total_liabilities:,.2f}", ln=1, align="R")
        pdf.set_font("Arial", size=12)

    add_account_section(equity_accounts, "EQUITY")
    total_equity = sum(equity_accounts.values()) if equity_accounts else 0
    if total_equity > 0:
        pdf.set_font("Arial", "B", size=12)  # Bold total
        pdf.cell(100, 10, txt="Total Equity", ln=0, align="L")
        pdf.cell(100, 10, txt=f"${total_equity:,.2f}", ln=1, align="R")
        pdf.set_font("Arial", size=12)

    total_liabilities_and_equity = total_liabilities + total_equity
    pdf.set_font("Arial", "B", size=12)  # Bold total
    pdf.cell(100, 10, txt="TOTAL LIABILITIES AND EQUITY", ln=0, align="L")
    pdf.cell(100, 10, txt=f"${total_liabilities_and_equity:,.2f}", ln=1, align="R")
    pdf.set_font("Arial", size=12)

    verification_result = (
        "Correct"
        if abs(total_assets - total_liabilities_and_equity) < 0.01
        else "Incorrect"
    )
    pdf.cell(
        200,
        10,
        txt=f"Verification: Assets = Liabilities + Equity: {verification_result}",
        ln=1,
        align="L",
    )

    pdf.output(filename)
    print(f"Balance sheet saved to {os.path.abspath(filename)}")

    webbrowser.open_new_tab("file://" + os.path.realpath(filename))




def generate_balance_sheet_html(balance_sheet_data, filename="balance_sheet.html"):
    """Generates an HTML file to display the balance sheet."""

    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S UTC")  # Format the date and time

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Balance Sheet</title>
        <style>
            body {{
                font-family: sans-serif;
            }}
            table {{
                width: 80%;
                margin: 20px auto;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .total-row {{
                font-weight: bold;
            }}
            .verification-row {{
                font-style: italic;
            }}
        </style>
    </head>
    <body>
        <h1>Balance Sheet</h1>
        <p>As of {date_string}</p>

        <table>
            <thead>
                <tr>
                    <th></th>
                    <th>Account</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
    """
    asset_accounts = balance_sheet_data.get("Asset", {})
    liability_accounts = balance_sheet_data.get("Liability", {})
    equity_accounts = balance_sheet_data.get("Equity", {})

    def add_account_section(accounts, section_title):
        nonlocal html_content  # Access the outer scope's html_content variable
        if accounts:
            html_content += f"<tr><td colspan='3'><strong>{section_title}</strong></td></tr>\n"  # Section header
            for account_name, amount in accounts.items():
                html_content += f"<tr><td></td><td>{account_name}</td><td>${amount:,.2f}</td></tr>\n"

    add_account_section(asset_accounts, "ASSETS")
    total_assets = sum(asset_accounts.values()) if asset_accounts else 0
    if total_assets > 0:
        html_content += f"<tr class='total-row'><td></td><td><strong>Total Assets</strong></td><td>${total_assets:,.2f}</td></tr>\n"

    add_account_section(liability_accounts, "LIABILITIES")
    total_liabilities = sum(liability_accounts.values()) if liability_accounts else 0
    if total_liabilities > 0:
        html_content += f"<tr class='total-row'><td></td><td><strong>Total Liabilities</strong></td><td>${total_liabilities:,.2f}</td></tr>\n"

    add_account_section(equity_accounts, "EQUITY")
    total_equity = sum(equity_accounts.values()) if equity_accounts else 0

    if total_equity > 0:  # Include Equity section if any data exists.
        html_content += f"<tr class='total-row'><td></td><td><strong>Total Equity</strong></td><td>${total_equity:,.2f}</td></tr>\n"

    total_liabilities_and_equity = total_liabilities + total_equity
    html_content += f"<tr class='total-row'><td></td><td><strong>TOTAL LIABILITIES AND EQUITY</strong></td><td>${total_liabilities_and_equity:,.2f}</td></tr>\n"

    verification_result = (
        "Correct"
        if abs(total_assets - total_liabilities_and_equity) < 0.01
        else "Incorrect"
    )
    html_content += f"<tr class='verification-row'><td></td><td>Verification: Assets = Liabilities + Equity</td><td>{verification_result}</td></tr>\n"
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(filename, "w") as f:
        f.write(html_content)

    print(f"Balance sheet saved to {os.path.abspath(filename)}")

    # Cross-platform way to open the HTML file
    url = "file://" + os.path.abspath(filename)
    webbrowser.open(url, new=2)  # new=2 opens in a new tab if possible


def main():
    try:
        balance_date_str = input("Enter balance sheet date (YYYY-MM-DD, or press Enter for most recent): ")
        balance_date = datetime.strptime(balance_date_str, "%Y-%m-%d").date() if balance_date_str else None
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return  # Or handle the error as you prefer


    balance_sheet_data = fetch_balance_sheet_data(balance_date)
    if balance_sheet_data:
        generate_balance_sheet_html(balance_sheet_data)
        download_choice = input("Download balance sheet as PDF? (yes/no): ")
        if download_choice.lower() == "yes":
	        generate_balance_sheet_pdf(balance_sheet_data)
             
if __name__ == "__main__":
    main()


