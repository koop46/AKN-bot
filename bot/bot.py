import tweepy
import schedule
import time
import openai
import yaml
import random

CREDS = yaml.load(open("credentials.yml"), Loader=yaml.FullLoader)

with open("Akash_info.txt", "r", encoding="utf-8") as file:
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
    

    def generate_tweet(self, model_choice, theme=AKASH_INFO):
        random_line = random.randint(10_000, 55_000)
#Developers building on decentralized clouds need persistent data storage that survives migrations. Akash Network�s Persistent Storage locks deployment data through lease cycles�while $SPICE fuels $AKT�s staking engine to scale network capacity. Build relentlessly. $SPICE $AKT

        prompt = f"""
        Generate a Twitter post based on following information: {theme}. 
The post must feature:  
1. Features 1 UNIQUE technical fact/statistic (verified by credible sources)  
2. Highlights a specific user need/pain point in tech/AI/development fields  
3. Shows how Akash Network's decentralized cloud uniquely solves this  
4. Includes $SPICE and $AKT with 2 synergistic hashtags from:  
[AI/ML cluster] OR [Dev/Engineering cluster] OR [Emerging Tech cluster] 
5. Start each post with a unique phrase that you didn't start with in older posts like: {old_posts} 
I suggest something from {AKASH_INFO[random_line:random_line+200]} that you haven't already posted about.

AVOID:  
- Using same opening phrase as in older posts, for reference check: {old_posts}  
- Using same first word in your new post that you have already used in older posts
- Using any derivative of first word in your new post that you have already used in older posts
- Price speculation/ROI claims  

TONE: Visionary architect revealing blueprints for next-gen tech infrastructure  

FORMULA:  
[Attention-grabbing fact or common values] + [User-centric problem statement] + [Akash-powered solution] + [Future-looking call to action] + $SPICE $AKT + [2 focused hashtags]  

Verify technical accuracy before finalizing.
Don't use same first word or any derivative of first word that you have already used in any other old post.
Don't use same first word or any derivative of first word that you have already used in any other old post.
Don't use same first word or any derivative of first word that you have already used in any other old post.
Don't use same first word or any derivative of first word that you have already used in any other old post.
Don't use same first word or any derivative of first word that you have already used in any other old post.
Don't use same first word or any derivative of first word that you have already used in any other old post.
Don't use same first word or any derivative of first word that you have already used in any other old post.
Don't use same first word or any derivative of first word that you have already used in any other old post.
Don't use same first word or any derivative of first word that you have already used in any other old post.

        """

        try:
            response = self.llm_client.chat.completions.create(
                model=model_choice,
                messages=[{"role": "user", "content": f"{prompt}. Only return answer without quotations and vary in theme/topic"}],
                temperature=0.7,
                max_tokens=2800
            )

            output = response.choices[0].message.content.strip()

            if model_choice == "DeepSeek-R1":
                _, output = output.split("</think>\n") 
            
            with open("old_posts.txt", "a") as file:
                file.write(f"\n{output}")
            
         #   print("random line", AKASH_INFO[random_line:random_line+2000])
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
    all_models = ["DeepSeek-R1", "Meta-Llama-3-3-70B-Instruct", "nvidia-Llama-3-1-Nemotron-70B-Instruct-HF"]

#    tweet = generator.generate_tweet(all_models[1])
    for model in all_models:
        tweet = generator.generate_tweet(model)

        if tweet != None:
            break
    print(tweet)
    
    client.post_tweet(tweet)
    

def generate_random_hours(n=5):
    return [f"{random.randint(0, 23):02}:{random.randint(0, 59):02}" for _ in range(n)]


def schedule_daily_events():
    schedule.clear()
    random_hours = generate_random_hours()
    print(random_hours)
    for hour in random_hours:
        schedule.every().day.at(hour).do(daily_post)




# Schedule the random hour generation at midnight
schedule.every().day.at("02:00").do(schedule_daily_events)

# Initial setup
schedule_daily_events()

# Run Continuously
while True:

    schedule.run_pending()
    print("Active!!!")
    time.sleep(60)

#daily_post()

