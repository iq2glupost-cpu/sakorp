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
    # 🔥 Supabase init OVDE (NE na vrhu fajla)
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        return jsonify({
            "success": False,
            "message": "Server config error"
        }), 500

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    data = request.get_json()

    email = data.get('email', '').strip().lower()
    source = data.get('source', 'unknown')

    # Validate email
    if not email or not is_valid_email(email):
        return jsonify({
            "success": False,
            "message": "Invalid email address"
        }), 400

    try:
        # Check if exists
        existing = supabase.table("waitlist") \
            .select("id") \
            .eq("email", email) \
            .execute()

        if existing.data:
            return jsonify({
                "success": False,
                "message": "Email already on the whitelist"
            }), 409

        # Insert
        supabase.table("waitlist").insert({
            "email": email,
            "source": source
        }).execute()

        return jsonify({
            "success": True,
            "message": "Added to whitelist"
        }), 200

    except Exception as e:
        print("ERROR:", str(e)) # 🔥 vidi log u Vercelu
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


# =========================
# RUN LOCAL
# =========================
if __name__ == '__main__':
    app.run(debug=True)
