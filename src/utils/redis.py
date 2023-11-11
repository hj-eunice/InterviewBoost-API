# system packages
import os

# third-party packages
import redis

# Connect to your internal Redis instance using the REDIS_URL environment variable
# The REDIS_URL is set to the internal Redis URL e.g. redis://red-343245ndffg023:6379
REDIS_SERVER = redis.from_url(os.environ['REDIS_URL'])
PREFIX = "InterviewBooster"

TTL=60*60


def save_transcript(user_id, question_num, transcript_txt):
    REDIS_SERVER.set(f"{PREFIX}-{user_id}-{question_num}", transcript_txt, ex=TTL)


def get_all_transcripts(user_id):
    transcripts = {}

    for i in range(1, 3):
        transcripts[i] = REDIS_SERVER.get(f"{PREFIX}-{user_id}-{i}").decode()

    return transcripts
