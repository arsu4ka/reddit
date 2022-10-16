import time, json, random
from models.redditClass import RedditProfile
import prawcore
from datetime import datetime


def get_weekday():
    return {
            "string": datetime.now().strftime('%A').lower(),
            "integer": datetime.now().weekday()
    }

def read_json(file_path):
    with open(file_path) as file:
        return json.load(file)
    

def write_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
    
def choose_flair(reddit: RedditProfile, community_name: str, weekday: str):
    try:
        if reddit.flair_required(community_name):
            options = reddit.flair_options(community_name)
            print(f"Flair required for community {community_name}, that will be posted on {weekday}")
            for index, option in enumerate(options):
                print(f"({index+1})  {option['name']}")
            return options[int(input("Choose flair option: ")) - 1]["id"]
    except prawcore.exceptions.Forbidden:
        return None
    
    
def sleep_until(time_equal):
    if time_equal == "now":
        return True
    if (datetime.now().hour > int(time_equal.split()[0])) or (datetime.now().hour == int(time_equal.split()[0]) and datetime.now().minute > int(time_equal.split()[1])):
        return False
    while time.strftime("%H:%M") != time_equal:
        time.sleep(10)
    return True


def post(reddit: RedditProfile, community: dict, media: dict):
    community_name = community["name"]
    time_to_sleep = community["blast_time"]
    flair_id = community["flair_id"]

    reddit.subscribe_if_not(community_name)

    if not sleep_until(time_to_sleep):
        return

    if community["override"]:   
        reddit.delete_previous_subreddits(community_name)
    submission = reddit.post_gallery_submission(media, community_name, flair_id)
    reddit.leave_comment(submission, media["comment"])
    print(f"{time.strftime('%H:%M%:%S')} Submission was successfully created from acc {reddit.user.me().name}, it's link: https://reddit.com{submission.permalink}")