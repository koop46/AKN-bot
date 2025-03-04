from datetime import datetime
import tweepy
import schedule
import time
import openai
import yaml
import random
from prompt import prompt_

CREDS = yaml.load(open("credentials.yml"), Loader=yaml.FullLoader)





### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


class ContentGenerator:

    """
    Initialize llm client
    
    """

    def __init__(self, CREDS):
        self.llm_client = openai.OpenAI(
            api_key=CREDS["AKASH_KEY"],
            base_url="https://chatapi.akash.network/api/v1"
        )
    

    def generate_tweet(self, model_choice):

        """
        1) feed prompt to modell
        2) split draft if modell == deepseek
        3) write to "old_posts" for reference
        4) return draft
        """


    

        try:
            response = self.llm_client.chat.completions.create(
                model=model_choice,
                messages=[{"role": "user", "content": f"{prompt_}. Only return answer without quotations"}],
                temperature=0.7,
                max_tokens=2800
            )

            output = response.choices[0].message.content.strip()

            if model_choice == "DeepSeek-R1":
                _, output = output.split("</think>\n") 
            
            with open("old_posts.txt", "a", encoding='utf-8') as file:
                file.write(f"\n{output}")
            
            return output

        except Exception as e:
            print(f"OpenAI Error: {e}")
            return None  # instead of crashing

    def verify_length(self, prompt):

        """
        1) load another model
        2) shorten draft
        3) return
        """

        response = self.llm_client.chat.completions.create(
        model="Meta-Llama-3-3-70B-Instruct",

        messages=[{"role": "user", "content": f"Verify that this text is below 280 characters: {prompt}. if it exceeds 280 characters edit it to be less than 280 characters. Edit as little as possible, leave as intact as you can. Only return answer without quotations"}],
        temperature=0.7,
        max_tokens=2800
        )

        output = response.choices[0].message.content.strip()
        print(output)

        return output

class TwitterClient:
    
    def __init__(self, CREDS):
        
        client_creds = {
        "consumer_key": CREDS["consumer_key"],
        "consumer_secret": CREDS["consumer_secret"],
        "access_token": CREDS["access_token"],
        "access_token_secret": CREDS["access_token_secret"]}

        # v1 for text posts, v2 for media posts
        self.v2 = tweepy.API(tweepy.OAuth1UserHandler(**client_creds))
        self.v1 = tweepy.Client(**client_creds)


    def post_tweet(self, text, media=None):
        try:
            if media:
                # Upload media and post tweet with both text and media
 #               media_obj = self.v2.media_upload(filename=media)
#                self.v1.create_tweet(text=text, media_ids=[media_obj.media_id])
                pass
            else:
                # Post text-only tweet
                self.v1.create_tweet(text=text)
                
            print(f"Posted: {text}" + (f" with media: {media}" if media else ""))
            
        except tweepy.TweepyException as e:
            print(f"Twitter error: {e}")



def daily_post():
    all_models = ["DeepSeek-R1", "Meta-Llama-3-3-70B-Instruct", "nvidia-Llama-3-1-Nemotron-70B-Instruct-HF"]

#    tweet = generator.generate_tweet(all_models[1])
    for model in all_models:
        draft = generator.generate_tweet(model)

        if draft != None:
            break
    post = generator.verify_length(draft)
#    client.post_tweet(post)
    

def generate_random_hours(n=5):
    return [f"{random.randint(0, 23):02}:{random.randint(0, 59):02}" for _ in range(n)]


def schedule_daily_events():
    schedule.clear()
    random_hours = generate_random_hours()

    with open("schedule.txt", "a", encoding='utf-8') as file:
        file.write(f"{datetime.today().strftime('%Y-%m-%d')}: {" --- ".join(random_hours)}\n")
    print(random_hours)

    for hour in random_hours:
        schedule.every().day.at(hour).do(daily_post)

# ### Test: 5 in a row
# for test in range(5):
#     daily_post()
#     print("------------")

generator = ContentGenerator(CREDS)
client = TwitterClient(CREDS)


# Schedule the random hour generation at midnight
schedule.every().day.at("00:00").do(schedule_daily_events)

# Initial setup
schedule_daily_events()

print("Creating first post...")
daily_post()


# Run Continuously
while True:

    schedule.run_pending()
    time.sleep(60)

#daily_post()


