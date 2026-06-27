from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder automatically if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Skills to check
SKILLS = [
    "python", "java", "c", "c++", "html", "css", "javascript",
    "react", "node", "sql", "mysql", "mongodb", "git",
    "docker", "aws", "machine learning", "ai"
]

# Function to extract text from PDF
def extract_text(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text.lower() + " "

    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]

    if file.filename == "":
        return "No file selected."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    text = extract_text(filepath)

    found_skills = []
    missing_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    ats_score = int((len(found_skills) / len(SKILLS)) * 100)

    return render_template(
        "result.html",
        score=ats_score,
        found=found_skills,
        missing=missing_skills
    )


if __name__ == "__main__":
    app.run(debug=True)