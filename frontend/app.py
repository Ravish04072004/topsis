from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import numpy as np
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import re
from datetime import datetime
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('results', exist_ok=True)


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_inputs(weights_str, impacts_str):
    """Validate weights and impacts format"""
    try:
        weights = [float(w.strip()) for w in weights_str.split(',')]
        impacts = [i.strip() for i in impacts_str.split(',')]
        
        if len(weights) != len(impacts):
            return False, "Number of weights and impacts must be equal"
        
        if not all(impact in ['+', '-'] for impact in impacts):
            return False, "Impacts must be '+' or '-'"
        
        return True, {"weights": weights, "impacts": impacts}
    except ValueError:
        return False, "Weights must be numeric values separated by commas"


def topsis_calculation(input_file, weights, impacts):
    """Perform TOPSIS calculation"""
    try:
        data = pd.read_csv(input_file)
        
        if data.shape[1] < 3:
            return False, "Error: Input file must contain at least 3 columns"
        
        matrix = data.iloc[:, 1:].values
        
        # Numeric check
        if not np.issubdtype(matrix.dtype, np.number):
            return False, "Error: From 2nd to last columns must be numeric"
        
        if len(weights) != matrix.shape[1] or len(impacts) != matrix.shape[1]:
            return False, "Error: Number of weights, impacts and columns must be same"
        
        # Normalization
        norm = np.sqrt((matrix ** 2).sum(axis=0))
        normalized = matrix / norm
        
        # Weighted normalized matrix
        weights_array = np.array(weights)
        weighted = normalized * weights_array
        
        # Ideal best & worst
        ideal_best = []
        ideal_worst = []
        
        for i in range(len(impacts)):
            if impacts[i] == '+':
                ideal_best.append(weighted[:, i].max())
                ideal_worst.append(weighted[:, i].min())
            else:
                ideal_best.append(weighted[:, i].min())
                ideal_worst.append(weighted[:, i].max())
        
        ideal_best = np.array(ideal_best)
        ideal_worst = np.array(ideal_worst)
        
        # Distance
        d_pos = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
        d_neg = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))
        
        # TOPSIS score
        score = d_neg / (d_pos + d_neg)
        
        data["Topsis Score"] = score
        data["Rank"] = data["Topsis Score"].rank(ascending=False).astype(int)
        
        return True, data
    
    except Exception as e:
        return False, f"Error during TOPSIS calculation: {str(e)}"


def send_email(recipient_email, result_file, filename):
    """Send email with result file attachment"""
    try:
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')

        # Check if credentials are set
        if not sender_email or not sender_password:
            return False, "Email credentials not configured in .env file"

        # Create email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = f"TOPSIS Analysis Results - {filename}"

        # Email body
        body = f"""
Dear User,

Your TOPSIS analysis has been completed successfully!

File: {filename}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

The results file with Topsis Score and Rank columns is attached.

Best regards,
TOPSIS Web Service
        """

        message.attach(MIMEText(body, "plain"))

        # Attach file
        with open(result_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(result_file)}")
        message.attach(part)

        # Send email - USE SMTP_SSL with port 465
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # server.starttls()  <-- DELETE THIS LINE (SSL does it automatically)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()

        return True, "Email sent successfully"

    except Exception as e:
        return False, f"Email sending failed: {str(e)}"
    
@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and TOPSIS calculation"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file provided"}), 400
        
        file = request.files['file']
        weights_str = request.form.get('weights', '').strip()
        impacts_str = request.form.get('impacts', '').strip()
        email = request.form.get('email', '').strip()
        
        # Validate inputs
        if not file.filename:
            return jsonify({"success": False, "message": "No file selected"}), 400
        
        if not weights_str or not impacts_str:
            return jsonify({"success": False, "message": "Weights and impacts are required"}), 400
        
        if not email:
            return jsonify({"success": False, "message": "Email is required"}), 400
        
        if not validate_email(email):
            return jsonify({"success": False, "message": "Invalid email format"}), 400
        
        # Validate weights and impacts
        is_valid, result = validate_inputs(weights_str, impacts_str)
        if not is_valid:
            return jsonify({"success": False, "message": result}), 400
        
        weights = result["weights"]
        impacts = result["impacts"]
        
        # Save uploaded file
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)
        
        # Perform TOPSIS calculation
        success, data = topsis_calculation(input_path, weights, impacts)
        if not success:
            return jsonify({"success": False, "message": data}), 400
        
        # Save result file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        result_filename = f"result_{timestamp}.csv"
        result_path = os.path.join('results', result_filename)
        data.to_csv(result_path, index=False)
        
        # Send email
        email_success, email_message = send_email(email, result_path, file.filename)
        
        response = {
            "success": True,
            "message": "TOPSIS analysis completed successfully!",
            "result_file": result_filename,
            "email_status": "Email sent successfully" if email_success else f"Warning: {email_message}",
            "data_preview": data.head(5).to_dict(orient='records'),
            "total_rows": len(data)
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download result file"""
    try:
        from flask import send_file
        result_path = os.path.join('results', filename)
        if not os.path.exists(result_path):
            return jsonify({"success": False, "message": "File not found"}), 404
        
        return send_file(result_path, as_attachment=True, download_name=filename)
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Download error: {str(e)}"}), 500


@app.route('/api/example')
def get_example():
    """Get example data"""
    example = {
        "weights": "1,1,1,1",
        "impacts": "+,+,-,+",
        "sample_data": "Fund Name,P1,P2,P3,P4\nM1,0.67,0.45,6.5,42.6\nM2,0.6,0.36,3.6,53.3\nM3,0.82,0.67,3.8,63.1\nM4,0.6,0.36,3.5,69.2"
    }
    return jsonify(example)


if __name__ == '__main__':
    app.run(debug=False)
