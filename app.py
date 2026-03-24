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
    try:
        data = request.get_json()
        print("DATA:", data)

        email = data.get('email', '').strip().lower()
        print("EMAIL:", email)

        if not email or not is_valid_email(email):
            return jsonify({
                "success": False,
                "message": "Invalid email"
            }), 400

        response = supabase.table("waitlist").insert({
            "email": email
        }).execute()

        print("SUPABASE RESPONSE:", response)

        return jsonify({
            "success": True
        }), 200

    except Exception as e:
        print("FULL ERROR:", str(e))
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500



# =========================
# RUN LOCAL
# =========================
if __name__ == '__main__':
    app.run(debug=True)
