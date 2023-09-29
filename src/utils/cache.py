# system packages
from collections import defaultdict
import os
import queue

# third-party packages
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
GEN_QUESTIONS_HOW_MANY = 5


""" example of the cache:
{
    "job_title_1": {
        "job_level_1": Queue(5),
        ...,
        "job_level_N": Queue(5)
    },
    ...,
    "job_title_N": {
        "job_level_1": Queue(5),
        ...,
        "job_level_N": Queue(5)
    },
}
"""
cached_starting_questions = defaultdict(lambda: defaultdict(queue.Queue))


def get_cached_starting_questions(job_title, job_level, n=1):
    if job_title not in cached_starting_questions or \
        job_level not in cached_starting_questions[job_title] or \
        cached_starting_questions[job_title][job_level].empty():
        # populate the cache
        new_questions = generate_starting_questions(job_title, job_level)
        for q in new_questions:
            cached_starting_questions[job_title][job_level].put(q)

    return cached_starting_questions[job_title][job_level].get()


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
    # print(response)

    res = [""] * GEN_QUESTIONS_HOW_MANY

    for choice in response.choices:
        res[choice.index] = choice.message.content

    # print(res)
    return res


def generate_prompt(job_title, job_level):
    return """Can you suggest me a creative behavioral question 
    I can ask to someone applying for the {} {} position?
    A question should be no longer than 200 characters.
    A question must not include any hashtags.
    Strip the first and last quotes.""".format(job_level, job_title)
