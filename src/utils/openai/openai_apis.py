# local packages
from utils.openai import openai

GEN_QUESTIONS_HOW_MANY = 5


def generate_starting_questions(job_title, job_level):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        n=GEN_QUESTIONS_HOW_MANY,
        messages=[
            {"role": "system", "content": "You suggest one creative question to interviewers who are working for IT companies."},
            {"role": "user", "content": generate_prompt(job_title, job_level)}
        ],
        stop=["#", "\n", "\\\""]
    )

    res = [""] * GEN_QUESTIONS_HOW_MANY

    for choice in response.choices:
        res[choice.index] = choice.message.content

    return res


def generate_prompt(job_title, job_level):
    return """Can you suggest me a creative behavioral question 
    I can ask to someone applying for the {} {} position?
    A question should be no longer than 200 characters.
    A question must not include any hashtags.
    Strip the first and last quotes.""".format(job_level, job_title)


def speech_to_text(audio_file):
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text
