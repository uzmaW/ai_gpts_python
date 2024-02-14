import os
import json
import requests
from openai import OpenAI
import time

import os
from dotenv import load_dotenv

load_dotenv()

# API keys are stored in Google Colab's Secret Manager
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FMP_API_KEY = os.getenv('FINANCE_PREP_API_KEY')

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["FMP_API_KEY"] = FMP_API_KEY

client = OpenAI()