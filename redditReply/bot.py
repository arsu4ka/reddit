import traceback
import praw
import json
from praw.models import Comment, Submission
import re
from datetime import datetime
from encrypt import encrypt

DEBUG = True

if DEBUG:
    json_path = "/Users/arsenijgoj/Developer/py/reddit/redditReply/settings.json"
else:
    json_path = input("Input path to your json settings file: ")

with open(json_path) as file:
    settings = json.load(file)
reddit = praw.Reddit(
    user_agent="test app",
    client_id=settings["client_id"],
    client_secret=settings["client_secret"],
    username=settings["username"],
    password=settings["password"]
)
try:
    print(f"Successfully started bot '{reddit.user.me()}'")
except:
    print(traceback.format_exc())
    print("Couldn't start the bot, check your credentials and console output.")
    exit()


def get_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")
 
 
def generate_reply(video_id) -> str:
    uri = encrypt("youtube", video_id)
    return f"# [View Link](https://mp3juice.fm/single/{uri})\n\n------------------------------------------------------------\n[DMCA](https://np.reddit.com/message/compose/?to=mp3juice_bot&subject=Content%20removal%20request%20for%20savevideo&message=https://np.reddit.com/) | [Contact](https://np.reddit.com/message/compose/?to=mp3juice_bot&subject=Contact&message=https://np.reddit.com/)"


def post_reply(comment: Comment, post: Submission = None):
    """
    func to find post where the comment is in and scrape YouTube links
    then generate reply using generate_reply() for all links and reply
    """
    if not post:
        post = comment.submission
    link_pattern = "(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
    youtube_ids = re.findall(link_pattern, post.selftext + post.url)
    result_string = ""
    for index, id in enumerate(youtube_ids):
        result_string += f"**[{index+1}]** *{generate_reply(id)}*\n"
    try:
        comment.reply(body=result_string)
    except:
        comment.reply(body="No youtube video here (((")


def main():
    count = 0
    try:
        while True:
            for mention in reddit.inbox.mentions():
                mention.refresh()
                mention.replies.replace_more()
                replied = False
                for reply in mention.replies:
                    if reply.author.name == reddit.user.me():
                        replied = True
                        break
                if not replied:
                    post_reply(comment=mention)
                    print(f"{get_time()} | Replied to mention under the {mention.submission.permalink}")
            if count % 10 == 0:
                print(f"{get_time()} | All mentions are replied")
            count += 1
    except Exception as ex:
        if ex == KeyboardInterrupt:
            exit()
        print(traceback.format_exc())
        print(f"{get_time()} | Error occurred while running the bot, check output earlier!")
        main()


if __name__ == "__main__":
    main()