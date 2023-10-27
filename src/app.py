# system packages
import base64
import tempfile

# third-party packages
from flask import Flask, jsonify, request
from flask_cors import CORS

# local packages
from utils.cache import get_cached_starting_questions
from utils.openai.openai_apis import speech_to_text

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
    temp_file = tempfile.NamedTemporaryFile(suffix=".webm")
    try:
        req_form = request.form
        decoded_data = base64.b64decode(req_form['fileBase64'])
        with open(temp_file.name, 'wb') as f:
            f.write(decoded_data)
        audio_file = open(temp_file.name, "rb")
        transcript = speech_to_text(audio_file)
    except Exception as e:
        print(e)
    finally:
        temp_file.close()

    return jsonify({
        "success": True,
        "transcript": transcript
    })


@app.route("/save", methods=["POST"])
def save_result():
    req_form = request.form

    return jsonify({
        "success": True,
        "transcript": request.form.get("transcript", ""),
        "raw_audio": request.files.get("rawAudio")
    })


if __name__ == '__main__':
    app.run()
