import os
from dotenv import load_dotenv
load_dotenv()

# 環境変数を参照
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
