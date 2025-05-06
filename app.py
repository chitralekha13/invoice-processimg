from flask import Flask, request, render_template
from main_orchestrator import run_invoice_pipeline
import os

app = Flask(__name__)
UPLOAD_FOLDER = "./data/invoices"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template("upload.html")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "❌ No file uploaded."
    file = request.files['file']
    if file.filename == '':
        return "❌ Empty filename."
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    print("📄 File saved:", filepath)
    result = run_invoice_pipeline(filepath)
    return result

if __name__ == '__main__':
    app.run(debug=True)
