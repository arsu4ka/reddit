import praw
from praw.reddit import Submission


class RedditProfile(praw.Reddit):
    
    def __init__(self, username, password, id, secret) -> None:
        super().__init__(
            user_agent=f"bot by u/{username}",
            client_id=id,
            client_secret=secret,
            username=username,
            password=password
        )

    def post_gallery_submission(self, media: dict, community, flair_id = None) -> Submission:
        title = media["title"]
        media = media["media"]
        return self.subreddit(community).submit_gallery(title, media, flair_id=flair_id)

    def subscribe_if_not(self, community):
        if not self.subreddit(community).user_is_subscriber:
            self.subreddit(community).subscribe()

    def flair_options(self, community) -> list:
        result = []
        for template in self.subreddit(community).flair.link_templates:
            result.append({"name": template["text"], "id": template["id"]})
        return result

    def delete_previous_subreddits(self, community):
        for submission in self.user.me().submissions.new():
            if submission.subreddit.display_name == community:
                submission.delete()

    def flair_required(self, community):
        return self.subreddit(community).post_requirements()["is_flair_required"]

    def leave_comment(self, post: Submission, text):
        """
        post: Submission to leave a reply
        text: Markdown formatted string
        """
        if not bool(text.strip()):
            return
        return post.reply(text)
    
