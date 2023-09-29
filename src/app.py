# third-party packages
from flask import Flask, jsonify, request
from flask_cors import CORS

# local packages
from utils.cache import get_cached_starting_questions

app = Flask(__name__)
CORS(app)


@app.route("/questions/first", methods=["POST"])
def generate_first_question():
    req_form = request.form
    job_title, job_level = req_form["job_title"], req_form["job_level"]
    print(job_title, job_level)

    question = get_cached_starting_questions(job_title, job_level)

    return jsonify({
        "success": True,
        "question": question,
        "job_title": job_title,
        "job_level": job_level
    })

if __name__ == '__main__':
    app.run()
