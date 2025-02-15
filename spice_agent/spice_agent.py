from pydantic_ai import Agent, RunContext
import tweepy
import schedule
import time
import yaml
from pydantic_ai.models.openai import OpenAIModel
from openai import AsyncOpenAI
from tools import generate_tweet, post_tweet, daily_post, llm_client



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


CREDS = yaml.load(open("credentials.yml"), Loader=yaml.FullLoader)
model = OpenAIModel("DeepSeek-R1", openai_client=llm_client)


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


akash_data_agent = Agent(
    model=model,
    system_prompt="""You are a senior data scientist, blockchain and cryptocurrency 
                    expert specialized in the Akash Network blockchain."""
)


x_post_agent = Agent(
    model = model,
    system_prompt= """You are a professional writer and sociala media marketer,
                     specialized in twitter/X plattform."""
)



@x_post_agent.tool
async def post_tweet(ctx: RunContext[None], daily_post):
    
        """Generate a new Twitter post from this texr: {theme}. Randomly pick any fact that might be interesting.
        Try to keep a excited but professional tone as if you know you're going to become rich.
        The post should be under 280 characters. Always include "$SPICE" and "$AKT" tickers at the end. 
        No Hashtags of any kind. No discussion about price or value

        Args:
            ctx: The context.
            daily_post: The function to trigger creation of.

        Return:
            str: The search results as a formatted string.

        """

