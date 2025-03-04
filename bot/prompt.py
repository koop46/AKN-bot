import random
from tags import ai_hashtags, dev_hashtags


with open("Akash_info.txt", "r", encoding="utf-8") as file:
    AKASH_INFO = file.read()


with open("old_posts.txt", "r", encoding='utf-8') as file:
    old_posts = file.read()




random_line = random.randint(10_000, 55_000)


prompt_ = f"""
        Generate a Twitter post based on following information: {AKASH_INFO}. 


The post must feature:  
1. Features 1 UNIQUE technical fact/statistic (verified by credible sources)  
I suggest something from {AKASH_INFO[random_line:random_line+1000]} that you haven't already posted about.
2. Highlights a specific user need/pain point in tech/AI/development fields  
3. Shows how Akash Network's decentralized cloud uniquely solves this  
4. Includes $SPICE and $AKT with 2 synergistic hashtags from {ai_hashtags, dev_hashtags}:  
[AI/ML cluster] OR [Dev/Engineering cluster] OR [Emerging Tech cluster].
5. Start each post with a unique phrase. Here's an example of posts with phrases you have used before that you must avoid: {old_posts}
6. Keep amount of characters in post to less than 280 characters.

AVOID:  
- Using same opening phrase as in older posts.  
- Using same first word in your new post that you have already used in older posts
- Using any derivative of first word in your new post that you have already used in older posts
- Price speculation/ROI claims  

TONE: Visionary architect revealing blueprints for next-gen tech infrastructure  

FORMULA:  
[Attention-grabbing fact or common values] + [User-centric problem statement] + [Akash-powered solution] + [Future-looking call to action] + $SPICE $AKT + [2 focused hashtags]  

Vary in theme/topic

Verify technical accuracy before finalizing.
Don't use same first word or any derivative of first word that you have already used in any other old post. Your post should not exceed 280 characters in length!


        """