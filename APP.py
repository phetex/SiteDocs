from flask import Flask, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

# Mock database
forms_db = []  # Stores forms data
compliance_db = []  # Tracks compliance
analytics_db = []  # Stores analyzed data

# Endpoint to create a site form
@app.route('/create_form', methods=['POST'])
def create_form():
    form = request.json
    form['id'] = len(forms_db) + 1
    forms_db.append(form)
    return jsonify({"message": "Form created successfully", "form_id": form['id']}), 201

# Endpoint to submit a form
@app.route('/submit_form', methods=['POST'])
def submit_form():
    form_submission = request.json
    form_submission['status'] = 'Submitted'
    compliance_db.append(form_submission)
    return jsonify({"message": "Form submitted successfully"}), 200

# Endpoint to monitor compliance
@app.route('/monitor_compliance', methods=['GET'])
def monitor_compliance():
    incomplete = [form for form in compliance_db if form['status'] != 'Completed']
    return jsonify({"incomplete_forms": incomplete}), 200

# Endpoint to analyze data
@app.route('/analyze_data', methods=['GET'])
def analyze_data():
    df = pd.DataFrame(compliance_db)
    summary = df['status'].value_counts().to_dict() if not df.empty else {}
    analytics_db.append(summary)
    return jsonify({"analytics_summary": summary}), 200

# Endpoint to integrate and share data
@app.route('/share_data', methods=['GET'])
def share_data():
    format_type = request.args.get('format', 'json')
    if format_type == 'csv':
        df = pd.DataFrame(forms_db)
        csv_data = df.to_csv(index=False)
        return csv_data, 200, {'Content-Type': 'text/csv'}
    return jsonify(forms_db), 200

# Sample data population
@app.route('/populate_sample_data', methods=['POST'])
def populate_sample_data():
    sample_forms = [
        {"title": "Safety Inspection", "fields": ["Inspector Name", "Date", "Observations"]},
        {"title": "Hazard Assessment", "fields": ["Hazard Type", "Location", "Severity"]}
    ]
    global forms_db
    forms_db.extend(sample_forms)
    return jsonify({"message": "Sample data added successfully"}), 201

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
