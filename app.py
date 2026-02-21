from flask import Flask, render_template, request
from analyzer import extract_text_from_pdf, compare

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():

    if request.method=="POST":

        job_text=request.form["job"]

        resume_file=request.files["resume"]
        resume_text=extract_text_from_pdf(resume_file)

        score,found,missing,job_skills=compare(resume_text,job_text)

        # build result object EXACTLY how your template expects
        result={
            "score":score,
            "resume_skills":found,
            "job_skills":job_skills,
            "missing":missing
        }

        return render_template("result.html", result=result)

    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)