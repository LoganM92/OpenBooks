from flask import Flask, request, jsonify
import os
import tempfile
from sql_utils.transaction_importer import parse_csv_and_insert_transactions


app = Flask(__name__)

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
        transaction_importer.parse_csv_and_insert_transactions(temp_filepath)


        # Delete the temporary file
        os.remove(temp_filepath)

        return jsonify({'success': True, 'message': 'File uploaded and processed successfully'}), 200
    except Exception as e:  # Catch any exceptions during processing
        return jsonify({'success': False, 'message': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)  # debug=True for development
