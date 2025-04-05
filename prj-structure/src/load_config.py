import os
from dotenv import load_dotenv

# Get the absolute path to the .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level from src
ENV_PATH = os.path.join(BASE_DIR, "config", ".env")

load_dotenv(dotenv_path=ENV_PATH, override=True)

test_env = os.getenv('TEST')

print(test_env)