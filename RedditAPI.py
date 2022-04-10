import praw
from psaw import PushshiftAPI
import pandas as pd
from datetime import datetime
from csv import reader
import time
import yaml

data = []
start = time.time()
folder = "API_keys.yaml"
subreddit = "CryptoCurrency"
after = datetime(2022, 4, 4).timestamp()

def yaml_loader(filepath):
    """Checks yaml file for API keys"""
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
    return data

def sec_to_hours(seconds):
    """Converts seconds to hours and minutes"""
    a=str(int(seconds//3600))
    b=str((int(seconds%3600)//60))
    c=str((int(seconds%3600)%60))
    d= "{} hours {} mins {} seconds".format(a, b, c)
    return d

def write(post):
    """Writes to CSV file"""
    df = pd.DataFrame(post)
    df.to_csv("DataSet.csv", mode = "a", sep =";", index=False, header=False)
    print("Writing...")
    
KEYS = yaml_loader(folder)

r = praw.Reddit(client_id = KEYS["client_id"],
        client_secret = KEYS["client_secret"],
        user_agent= KEYS["user_agent"], 
        check_for_async=False)

api=PushshiftAPI(r)

for i in  range(180):
    before = datetime.fromtimestamp(after - 86400 - 1) #Start of interval to gather posts from Reddit
    dd = datetime.fromtimestamp(after) #End of interval
    subs = api.search_submissions(after= before, before=dd, subreddit=[subreddit], limit=1000) #Request
    df = pd.DataFrame([sub.__dict__ for sub in subs])
    for col_name, d in df.iterrows():
        data.append([d["created"], d["title"], d["author"], d["selftext"], d["link_flair_text"], d["score"], d["num_comments"]])
    if len(data) != 0:
        write(data)
        print("Working for:", sec_to_hours(time.time() - start), "seconds.")
        print("Gathered data from ", before, "to", datetime.fromtimestamp(after))
    after = after - 86400
    data = []

print("over...")
        