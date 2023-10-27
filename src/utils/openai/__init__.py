# system packages
import os

# third-party packages
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
