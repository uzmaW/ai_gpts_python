import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FMP_API_KEY = os.getenv('FINANCE_PREP_API_KEY')

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["FMP_API_KEY"] = FMP_API_KEY

