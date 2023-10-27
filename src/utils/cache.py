# system packages
from collections import defaultdict
import os
import queue

from utils.openai.openai_apis import generate_starting_questions

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
