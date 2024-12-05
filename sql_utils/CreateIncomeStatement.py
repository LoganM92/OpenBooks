import MySQLdb
from datetime import datetime, date
from fpdf import FPDF
import webbrowser
import os

# Database connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"
DB_NAME = "my_new_database"  

# Connect to the database
def connect_to_db():
    return MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME
    )



def generate_income_statement(start_date, end_date):
    """
    Generates an income statement for the specified period.

    Args:
        start_date (date): The start date of the reporting period.
        end_date (date): The end date of the reporting period.

    Returns:
        tuple: A tuple containing two dictionaries. The first contains the income statement data,
               and the second contains totals (revenue, expenses, net income).  Returns 
               None if there is a database error or if the input dates are invalid.
    """

    if start_date > end_date:
        return None, "Invalid date range: Start date must be before end date."  # Handle invalid date range


    conn = connect_to_db()
    if not conn:
        return None, "Database connection error."


    cursor = conn.cursor()

    try:
        # Get all account IDs and names (no filtering by account type)
        cursor.execute("SELECT id, account_name FROM ChartOfAccounts;")
        accounts = dict(cursor.fetchall())

        income_statement_data = {"Revenue": {}, "Expenses": {}}  # Initialize

        for account_id, account_name in accounts.items():
            cursor.execute(
                """
                SELECT SUM(received) AS total_received, SUM(spent) AS total_spent
                FROM Transactions
                WHERE chart_of_accounts_id = %s
                  AND date >= %s
                  AND date <= %s;
                """,
                (account_id, start_date, end_date),
            )
            result = cursor.fetchone()

            total_received = result[0] or 0
            total_spent = result[1] or 0
            net_amount = total_received - total_spent

            if net_amount > 0:  # Positive is revenue
                income_statement_data["Revenue"][account_name] = net_amount
            elif net_amount < 0:  # Negative is expense
                income_statement_data["Expenses"][account_name] = abs(net_amount) # Store as positive


        # Calculate totals (remains the same)
        total_revenue = sum(income_statement_data.get("Revenue", {}).values())
        total_expenses = sum(income_statement_data.get("Expenses", {}).values())

        net_income = total_revenue - total_expenses

        totals = {
            "Total Revenue": total_revenue,
            "Total Expenses": total_expenses,
            "Net Income": net_income,
        }

        return income_statement_data, totals

    except Exception as e:
        return None, str(e)  # Return None and the error message

    finally:
        if cursor:
            cursor.close()
        if conn and conn.open:
            conn.close()
            
            
            
            
def generate_income_statement_pdf(income_statement_data, totals, start_date, end_date, filename="income_statement.pdf"):
    print("Income Statement Data:", income_statement_data)
    print("Totals:", totals) # You can print the totals as well
    """Generates a PDF of the income statement."""

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style="B", size=16)  # Bold title
    pdf.cell(200, 10, txt="Income Statement", ln=1, align="C")
    date_str = f"For the period {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=date_str, ln=1, align="C") # Add date range

    pdf.ln(10) # Add some spacing after title


    def add_section(data, title):
        pdf.set_font("Arial", style="B", size=14)  # Bold section title
        pdf.cell(200, 10, txt=title, ln=1, align="L")
        pdf.set_font("Arial", size=12)  # Back to normal font

        for account_name, amount in data.items():
            pdf.cell(100, 10, txt=account_name, ln=0, align="L")
            pdf.cell(100, 10, txt=f"${amount:,.2f}", ln=1, align="R")
        pdf.ln(5) # Small space between accounts


    if "Revenue" in income_statement_data:
        add_section(income_statement_data["Revenue"], "Revenue")

    if "Expenses" in income_statement_data:
        add_section(income_statement_data["Expenses"], "Expenses")

    pdf.line(pdf.l_margin, pdf.get_y(), 210 - pdf.r_margin, pdf.get_y()) # Line between Expenses and Net Income

    # Totals
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(100, 10, txt="Net Income:", ln=0, align="L")
    pdf.cell(100, 10, txt=f"${totals['Net Income']:,.2f}", ln=1, align="R")

    pdf.output(filename)


    webbrowser.open_new_tab("file://" + os.path.realpath(filename))
    print(f"Income statement PDF saved to: {os.path.abspath(filename)}")
