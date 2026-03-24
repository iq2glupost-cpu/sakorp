from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Servira index.html iz foldera 'templates'
    return render_template('index.html')

# Vercel koristi 'app' instancu, ovo je za lokalno testiranje
if __name__ == '__main__':
    app.run(debug=True)

