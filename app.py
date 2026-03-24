from flask import Flask, render_template, request, jsonify
from supabase import create_client
import os
import re

app = Flask(__name__)

# =========================
# EMAIL VALIDATION
# =========================
def is_valid_email(email):
    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    return re.match(pattern, email)


# =========================
# ROUTES
# =========================
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/whitelist', methods=['POST'])
def whitelist():
    data = request.get_json()

    email = data.get('email', '').strip().lower()

    if not email or not is_valid_email(email):
        return jsonify({
            "success": False,
            "message": "Invalid email address"
        }), 400

    try:
        supabase.table("waitlist").insert({
            "email": email
        }).execute()

        return jsonify({
            "success": True,
            "message": "Added to whitelist"
        }), 200

    except Exception as e:
        print("ERROR:", str(e)) # 👈 OVO JE KLJUČNO
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


# =========================
# RUN LOCAL
# =========================
if __name__ == '__main__':
    app.run(debug=True)
