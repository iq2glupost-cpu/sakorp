from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import os

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

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


@app.route("/waitlist", methods=["POST"])
def waitlist():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({
            "status": "error",
            "message": "Email je obavezan."
        }), 400

    try:
        response = supabase.table('waitlist').insert({"email": email}).execute()
        return jsonify({
            "status": "success",
            "message": "Uspešno dodato na listu!"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# =========================
# RUN LOCAL
# =========================
if __name__ == '__main__':
    app.run(debug=True)
