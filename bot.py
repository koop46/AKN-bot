import tweepy
import schedule
import time
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Read Akash Info from file once
with open("Akash_info.txt", "r") as file:
    AKASH_INFO = file.read()

# API Credentials
AKASH_API_KEY = os.getenv("AKASH_KEY")  
CREDS = {
    "consumer_key": os.getenv("API_KEY"),
    "consumer_secret": os.getenv("API_SECRET"),
    "access_token": os.getenv("ACCESS_TOKEN"),
    "access_token_secret": os.getenv("ACCESS_TOKEN_SECRET")
}

class ContentGenerator:
    def __init__(self):
        self.llm_client = openai.OpenAI(
            api_key=AKASH_API_KEY,
            base_url="https://chatapi.akash.network/api/v1"
        )
    
    def generate_tweet(self, theme=AKASH_INFO):
        prompt = f"""Generate a new Twitter post from this texr: {theme}. 
        The post should be under 280 characters. Always include "$SPICE" and "$AKT" tickers at the end. 
        No Hashtags of any kind. No discussion about price or value"""

        try:
            response = self.llm_client.chat.completions.create(
                model="DeepSeek-R1",
                messages=[{"role": "user", "content": f'{prompt}. Only return post text, without quotation marks.'}],
                temperature=0.7,
                max_tokens=2800
            )

            raw_output = response.choices[0].message.content.strip()
            _, output = raw_output.split("</think>\n") 
            return output

        except Exception as e:
            print(f"OpenAI Error: {e}")
            return None  # instead of crashing


class TwitterClient:
    def __init__(self):
        self.client = tweepy.Client(
            consumer_key=CREDS["consumer_key"], 
            consumer_secret=CREDS["consumer_secret"],
            access_token=CREDS["access_token"], 
            access_token_secret=CREDS["access_token_secret"]
        )

    def post_tweet(self, text):
        try:
            self.client.create_tweet(text=text)
            
            print(f"Posted: {text}")
        except tweepy.TweepyException as e:
            print(f"Twitter error: {e}")

generator = ContentGenerator()
client = TwitterClient()

def daily_post():
    
    tweet = generator.generate_tweet()
    client.post_tweet(tweet)
    
 
# # # Schedule Setup
# schedule.every().day.at("13:23").do(daily_post)
# schedule.every().day.at("13:24").do(daily_post)

# # # # Run Continuously
# while True:
#     schedule.run_pending()
#     time.sleep(60)

daily_post()