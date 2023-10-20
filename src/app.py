# system packages
import base64

# third-party packages
from flask import Flask, jsonify, request
from flask_cors import CORS

# local packages
from utils.cache import get_cached_starting_questions
from utils.speech_to_text import speech_to_text

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


@app.route("/transcribe", methods=["POST"])
def transcribe():
    transcript = ""
    try:
        req_form = request.form
        decoded_data = base64.b64decode(req_form['fileBase64'])
        with open('/tmp/audio.webm', 'wb') as f:
            f.write(decoded_data)
        audio_file = open('/tmp/audio.webm', "rb")
        transcript = speech_to_text(audio_file)
    except Exception as e:
        print(e)

    return jsonify({
        "success": True,
        "transcript": transcript
    })

if __name__ == '__main__':
    app.run()
