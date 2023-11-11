# system packages
import base64
import tempfile
import uuid

# third-party packages
from flask import Flask, jsonify, request
from flask_cors import CORS

# local packages
from utils.cache import get_cached_starting_questions
from utils.openai.openai_apis import speech_to_text
from utils import redis

app = Flask(__name__)
CORS(app)


@app.route("/questions/first", methods=["POST"])
def generate_first_question():
    req_form = request.form
    job_title = req_form["job_title"], 
    job_level = req_form.get("job_level", "")
    print(job_title, job_level)

    question = get_cached_starting_questions(job_title, job_level)

    return jsonify({
        "success": True,
        "question": question,
        "job_title": job_title,
        "job_level": job_level,
        "id": str(uuid.uuid4())
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


@app.route("/submit", methods=["POST"])
def submit_answer():
    req_form = request.form
    user_id = req_form.get("id")

    # save transcript to redis
    question_num = req_form.get("question")
    transcript = req_form.get("transcript", "")
    redis.save_transcript(user_id, question_num, transcript)

    # TODO save audio in filesystem

    # TODO next question
    question = "Why do you want to work for us?"

    return jsonify({
        "success": True,
        "id": user_id,
        "question": question,
    })


@app.route("/results", methods=["POST"])
def results():
    req_form = request.form
    user_id = req_form.get("id")

    # save transcript to redis
    question_num = req_form.get("question")
    transcript = req_form.get("transcript", "")
    redis.save_transcript(user_id, question_num, transcript)

    transcripts = redis.get_all_transcripts(user_id)

    return jsonify({
        "success": True,
        "id": user_id,
        "answers": transcripts,
    })


if __name__ == '__main__':
    app.run()
