import os
from dotenv import load_dotenv


load_dotenv()


APP_NAME = "InsightAI"
APP_TAGLINE = "Your Multi-Role Intelligent Assistant"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DEFAULT_MODEL = "gpt-6-luna"