import tweepy
import schedule
import time
import openai
import yaml

CREDS = yaml.load(open("credentials.yml"), Loader=yaml.FullLoader)

with open("Akash_info.txt", "r") as file:
    AKASH_INFO = file.read()

with open("old_posts.txt", "r") as file:
    old_posts = file.read()

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


class ContentGenerator:

    def __init__(self, CREDS):
        self.llm_client = openai.OpenAI(
            api_key=CREDS["AKASH_KEY"],
            base_url="https://chatapi.akash.network/api/v1"
        )
    

    def generate_tweet(self, theme=AKASH_INFO):
#Developers building on decentralized clouds need persistent data storage that survives migrations. Akash Network�s Persistent Storage locks deployment data through lease cycles�while $SPICE fuels $AKT�s staking engine to scale network capacity. Build relentlessly. $SPICE $AKT
        prompt = f"""
        Generate a new Twitter post from this texr: {theme}. Randomly pick any fact that might be interesting.
        But it has to be as disimilar to these posts as possible: {old_posts}.
        Include people's need when you craft your posts and suggest 1 way in which Akash Network can help fullfilling that need. 
        And make sure any claim is verifiable.
        
        Try to keep a excited but professional tone as if you know you're going to become rich.
        The post should be under 280 characters. Always include "$SPICE" and "$AKT" tickers at the end. 
        No Hashtags of any kind. No discussion about price or value
        """

        try:
            response = self.llm_client.chat.completions.create(
                model="DeepSeek-R1",
                messages=[{"role": "user", "content": f'{prompt}. Only return post text, without quotation marks.'}],
                temperature=0.7,
                max_tokens=2800
            )

            raw_output = response.choices[0].message.content.strip()
            _, output = raw_output.split("</think>\n") 
            
            with open("old_posts.txt", "a") as file:
                file.write(f"\n{output}")
            
            
            return output

        except Exception as e:
            print(f"OpenAI Error: {e}")
            return None  # instead of crashing


class TwitterClient:
    
    def __init__(self, CREDS):
        
        client_creds = {
        "consumer_key": CREDS["consumer_key"],
        "consumer_secret": CREDS["consumer_secret"],
        "access_token": CREDS["access_token"],
        "access_token_secret": CREDS["access_token_secret"]}

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


generator = ContentGenerator(CREDS)
client = TwitterClient(CREDS)

def daily_post():
    
    tweet = generator.generate_tweet()
    client.post_tweet(tweet, "spice_art.png")
    
 
# # # Schedule Setup
# schedule.every().day.at("13:23").do(daily_post)
# schedule.every().day.at("13:24").do(daily_post)
# schedule.every().day.at("13:23").do(daily_post)
# schedule.every().day.at("13:24").do(daily_post)
# schedule.every().day.at("13:24").do(daily_post)

# # # # Run Continuously
# while True:
#     schedule.run_pending()
#     time.sleep(60)

daily_post()

