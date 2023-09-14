import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv(override=True)
openai.api_key = os.getenv("OPEN_AI_KEY")
