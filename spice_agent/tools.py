import yaml
import tweepy
import openai


CREDS = yaml.load(open("credentials.yml"), Loader=yaml.FullLoader)

with open("Akash_info.txt", "r") as file:
    AKASH_INFO = file.read()


########################################################################
########################################################################
########################################################################


def generate_tweet(theme=AKASH_INFO):
    
    prompt = f"""Generate a new Twitter post from this texr: {theme}. Randomly pick any fact that might be interesting.
    Try to keep a excited but professional tone as if you know you're going to become rich.
    The post should be under 280 characters. Always include "$SPICE" and "$AKT" tickers at the end. 
    No Hashtags of any kind. No discussion about price or value"""

    try:
        response = llm_client.chat.completions.create(
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


def post_tweet( text, media=None):
    try:
        if media:
            # Upload media and post tweet with both text and media
            media_obj = v2.media_upload(filename=media)
            v1.create_tweet(text=text, media_ids=[media_obj.media_id])
        else:
            # Post text-only tweet
            v1.create_tweet(text=text)
            
        print(f"Posted: {text}" + (f" with media: {media}" if media else ""))
        
    except tweepy.TweepyException as e:
        print(f"Twitter error: {e}")


def daily_post(generator, client):
    
    tweet = generator.generate_tweet()
    client.post_tweet(tweet, "spice_art.png")
    


########################################################################
########################################################################
########################################################################


client_creds = {
"consumer_key": CREDS["consumer_key"],
"consumer_secret": CREDS["consumer_secret"],
"access_token": CREDS["access_token"],
"access_token_secret": CREDS["access_token_secret"]}

v2 = tweepy.API(tweepy.OAuth1UserHandler(**client_creds))
v1 = tweepy.Client(**client_creds)



llm_client = openai.OpenAI(
    api_key=CREDS["AKASH_KEY"],
    base_url="https://chatapi.akash.network/api/v1"
)