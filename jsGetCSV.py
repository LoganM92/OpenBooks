from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile
from datetime import datetime, date
from sql_utils.ImportCSV import parse_csv_and_insert_transactions
from sql_utils.AddAccount import add_account
from sql_utils.CreateIncomeStatement import generate_income_statement, generate_income_statement_pdf





app = Flask(__name__)
@app.route('/')
def index():
    return render_template('login.html')
    
    
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'csv_file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400

    file = request.files['csv_file']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400


    if not file.filename.lower().endswith('.csv'):
        return jsonify({'success': False, 'message': 'File must be a CSV'}), 400
    try:    
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            file.save(temp_file.name)
            temp_filepath = temp_file.name

        # Process the CSV
        parse_csv_and_insert_transactions(temp_filepath)


        # Delete the temporary file
        os.remove(temp_filepath)

        return jsonify({'success': True, 'message': 'File uploaded and processed successfully'}), 200
    except Exception as e:  # Catch any exceptions during processing
        return jsonify({'success': False, 'message': str(e)}), 500



@app.route('/add_account', methods=['POST'])
def add_account_route():
    data = request.get_json()

    account_name = data.get("account_name")
    account_type = data.get("account_type")
    account_subtype = data.get("account_subtype")

    if not account_name or not account_type:  # Basic validation
        return jsonify({"success": False, "message": "Account name and type are required."}), 400

    success, message = AddAccount.add_account(account_name, account_type, account_subtype) # Returns tuple

    return jsonify({"success": success, "message": message})




@app.route('/tabs')
def tabs():
    return render_template('tabs.html')  

@app.route('/home')
def home():
    return render_template('tab_0.html')

@app.route('/overlook')
def overlook():
    return render_template('tab_1.html')

@app.route('/balance_sheet')
def balance_sheet():
    return render_template('tab_2.html')

@app.route('/tab_3')
def tab_3():
    return render_template('tab_3.html')

@app.route('/tab_4', methods=['GET', 'POST'])
def income_statement():
    print(request.form)
    if request.method == 'POST':
        try:
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')


            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()



            income_statement_data, totals = generate_income_statement(start_date, end_date)

            if income_statement_data:
                try:
                    pdf_filename = "income_statement.pdf"


                    generate_income_statement_pdf(
                        income_statement_data, totals, start_date, end_date, pdf_filename
                    )

                    pdf_filepath = os.path.join(app.root_path, pdf_filename)


                    return send_file(pdf_filepath, as_attachment=True)

                except Exception as e:
                    return jsonify({"success": False, "message": str(e)}), 500
            else:
                return jsonify({"success": False, "message": totals}), 500


        except ValueError:
            return jsonify({"success": False, "message": "Invalid date format. Please use YYYY-MM-DD."}), 400

    return render_template('tab_4.html')

@app.route('/tab_5')
def tab_5():
    return render_template('tab_5.html')    

@app.route('/tab_6')
def tab_6():
    return render_template('tab_6.html')   

@app.route('/tab_5')
def tab_5():
    return render_template('tab_5.html')    

@app.route('/tab_6')
def tab_6():
    return render_template('tab_6.html')   

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    
    return render_template('tab_0.html')      
    
if __name__ == '__main__':
    app.run(debug=True)
