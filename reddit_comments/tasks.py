import praw

from celery.task import task, periodic_task
from celery.schedules import crontab

from reddit_comments.models import Submission, Comment, TrollClassifierWeights,
from reddit_comments.troll_classifier import classify_comment_content_for_troll

import settings

import logging
logger = logging.getLogger(__name__)

reddit = praw.Reddit(user_agent=settings.REDDIT_USER_AGENT)
reddit.login(username=settings.REDDIT_USERNAME,
             password=settings.REDDIT_PASSWORD)
search_subreddits = (
    'politics',
    'funny',
    'gaming',
    'atheism',
    'trees',
    'starcraft',
    'anime'
)


@periodic_task(run_every=crontab(minute="*/15"))
def search_subreddits_for_trolls():
    """
    Crawl the subreddits for trolls
    """
    for subreddit in subreddits:
        search_subreddit_for_trolls.delay(subreddit)


@task
def search_subreddit_for_trolls(subreddit, post_limit=15):
    """
    Given a sub reddit, will go through all the <post_limit> posts searching
    for troll comments
    """
    submissions = reddit.get_subreddit(subreddit).get_hot(limit=post_limit)
    for submission in submissions:
        search_post_for_trolls.delay(submission)


@task
def search_post_for_trolls(post):
    """
    Given a post will search through all the comments for troll posts. If a
    troll post is found, it will save the post to mongo so that a reply can be
    made later
    """
    for comment in post.all_comments:
        is_troll_post = classify_comment_content_for_troll(comment.body)
        if is_troll_post:
            logger.info("Saved troll comment %s to db" % comment.id)
            submission = Submission(id=comment.submission.id,
                                    title=comment.submission.title,
                                    permalink=comment.submission.permalink,
                                    url=comment.submission.url)
            submission.save()
            Comment(id=comment.id,
                    author_id=comment.author.id,
                    author_name=comment.author.name,
                    body=comment.body,
                    body_html=comment.body_html,
                    permalink=comment.permalink,
                    submission=submission).save()
