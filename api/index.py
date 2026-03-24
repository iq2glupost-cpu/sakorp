from flask import Flask, render_template, request, jsonify
from supabase import create_client
import os
import re

app = Flask(__name__, template_folder='../templates')

# =========================
# SUPABASE
# =========================
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)
print("URL:", url)
print("KEY:", key)


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

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route('/whitelist', methods=['POST'])
def whitelist():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()

        if not email or not is_valid_email(email):
            return jsonify({"success": False}), 400

        supabase.table("waitlist").insert({
            "email": email
        }).execute()

        return jsonify({"success": True})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"success": False}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5010)
