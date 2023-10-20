# system packages
import os

# third-party packages
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def speech_to_text(audio_file):
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text
