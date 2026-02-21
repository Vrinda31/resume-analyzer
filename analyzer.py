import PyPDF2
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(file):

    filename=file.filename.lower()

    # TXT SUPPORT
    if filename.endswith(".txt"):
        return file.read().decode("utf-8")

    # PDF SUPPORT
    if filename.endswith(".pdf"):
        try:
            reader=PyPDF2.PdfReader(file)
            text=""
            for page in reader.pages:
                if page.extract_text():
                    text+=page.extract_text()
            return text
        except:
            return ""

    return ""

def compare(resume,job):

    #master skills list
    skills=["python","java","sql","flask","django","html","css","javascript",
            "machine learning","data","git","react","api","pandas","numpy"]

    resume_lower=resume.lower()
    job_lower=job.lower()

    #exact match in resume
    resume_skills=[s for s in skills if re.search(r'\b{}\b'.format(re.escape(s)), resume_lower)]

    #exact match in job description
    job_skills = [s for s in skills if re.search(r'\b{}\b'.format(re.escape(s)), job_lower)]

    #skills found in job and resume
    matched=[s for s in job_skills if s in resume_skills]

    #skills missing from resume
    missing=[s for s in job_skills if s not in resume_skills]

    #skill based score
    score = round((len(matched) / len(job_skills) * 100), 2) if job_skills else 0
    
    return score, resume_skills, missing, job_skills