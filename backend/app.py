from flask import Flask, render_template, request, redirect, url_for, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

from resume_parser import extract_text, analyze_resume
from database import create_database, register_user, login_user

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

create_database()

# Store the latest resume analysis result
latest_result = {}


# ---------------- HOME ----------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            return "Passwords do not match."

        success = register_user(fullname, email, password)

        if success:
            return redirect(url_for("login"))
        else:
            return "Email already registered."

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = login_user(email, password)

        if user:
            return redirect(url_for("upload"))
        else:
            return "Invalid Email or Password."

    return render_template("login.html")


# ---------------- UPLOAD PAGE ----------------

@app.route("/upload", methods=["GET"])
def upload():
    return render_template("upload.html")


# ---------------- RESUME ANALYSIS ----------------

@app.route("/upload", methods=["POST"])
def upload_resume():

    global latest_result

    if "resume" not in request.files:
        return "No file uploaded."

    file = request.files["resume"]

    if file.filename == "":
        return "No file selected."

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(filepath)

    text = extract_text(filepath)

    result = analyze_resume(text)

    # Save latest result for PDF download
    latest_result = result

    return render_template(
        "result.html",
        score=result["score"],
        skills=result["skills"],
        missing=result["missing"],
        suggestions=result["suggestions"],
        questions=result["questions"]
    )


# ---------------- DOWNLOAD PDF ----------------

@app.route("/download")
def download():

    global latest_result

    if not latest_result:
        return "No report available. Please analyze a resume first."

    filename = "Resume_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("AI Resume Analyzer Report", styles["Heading1"]))
    story.append(Paragraph(f"ATS Score : {latest_result['score']}%", styles["Heading2"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("Skills Found", styles["Heading2"]))

    for skill in latest_result["skills"]:
        story.append(Paragraph("• " + skill, styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("Missing Skills", styles["Heading2"]))

    for skill in latest_result["missing"]:
        story.append(Paragraph("• " + skill, styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("Suggestions", styles["Heading2"]))

    for suggestion in latest_result["suggestions"]:
        story.append(Paragraph("• " + suggestion, styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("Interview Questions", styles["Heading2"]))

    for question in latest_result["questions"]:
        story.append(Paragraph("• " + question, styles["Normal"]))

    doc.build(story)

    return send_file(filename, as_attachment=True)


# ---------------- MAIN ----------------

if __name__ == "__main__":
    app.run(debug=True)