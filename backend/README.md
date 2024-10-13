Must add a .env with Following:


DATABRICKS_API_URL=https://<your-databricks-instance>/api/2.0/
DATABRICKS_TOKEN=<your-databricks-token>
CHATGPT_API_URL= 'https://api.openai.com/v1/chat/completions'
CHATGPT_API_KEY=Key can be found at openai.com but for this project will be in discord group....


Must also edit the config.py file as such:

# config/config.py

import os

from dotenv import load_dotenv
load_dotenv()


DATABRICKS_API_URL = os.getenv("DATABRICKS_API_URL", "https://<your-databricks-instance>/api/2.0/")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN", "<your-databricks-token>")

CHATGPT_API_URL = os.getenv("CHATGPT_API_URL", "https://api.openai.com/v1/chat/completions")
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY", "")