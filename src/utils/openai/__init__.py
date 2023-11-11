# system packages
import os

# third-party packages
from openai import OpenAI

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
