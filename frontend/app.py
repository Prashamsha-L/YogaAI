from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# -----------------------
# CONFIGURATION - UPDATE THESE
# -----------------------
gmail_user = "yogaai.contact@gmail.com"       # <-- Your Gmail (sender)
gmail_app_password = "yawotimctszjrmgx"      # <-- 16-digit App Password
receiver_email = "yogaai.contact@gmail.com"   # <-- Where you want to receive messages
# -----------------------

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Accept form-data from HTML
        data = request.form if request.form else (request.get_json() or {})

        # Get values from form
        name = data.get('name')
        sender_email = data.get('email')  # user email from form
        message = data.get('message')

        # Validate inputs
        if not name or not sender_email or not message:
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        # Prepare email
        subject = f"📩 New Message from {name} (YogaAI Contact Form)"
        current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        email_content = f"""
New message received from YogaAI Contact Page:

Name: {name}
Email: {sender_email}
Sent at: {current_time}

💬 Message:
{message}
"""

        # Create MIME email
        msg = MIMEText(email_content)
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = receiver_email
        msg['Reply-To'] = sender_email  # Reply will go to user

        # Send email via Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_app_password)
            server.send_message(msg)

        # Optional: log messages locally
        with open("contact_log.txt", "a") as f:
            f.write(f"{current_time} - {name} ({sender_email}): {message}\n")

        return jsonify({"success": True, "message": "Email sent successfully!"})

    except Exception as e:
        print("Error sending email:", e)
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)