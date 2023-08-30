import os

import openai
from flask import Flask, jsonify, request

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/questions/first", methods=["POST"])
def generate_first_question():
    req_form = request.form
    job_title, job_level = req_form["job_title"], req_form["job_level"]
    print(job_title, job_level)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You suggest one creative question to interviewers who are working for IT companies."},
            {"role": "user", "content": generate_prompt(job_title, job_level)}
        ]
    )
    # print(response)

    return jsonify({
        "success": True,
        "question": response.choices[0].message.content,
        "job_title": job_title,
        "job_level": job_level
    })


def generate_prompt(job_title, job_level):
    return """Can you give me an example of the behavioral question 
    I can ask to someone applying for the {} {} position?
    The question should be no longer than 200 characters.
    No hash tag should be included.""".format(job_level, job_title)
