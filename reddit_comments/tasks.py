import praw

from celery.task import task, periodic_task
from celery.schedules import crontab

from reddit_comments.models import troll_model, feature_words, save_submission_and_comment
from reddit_comments import troll_classifier

import settings

import logging
logger = logging.getLogger(__name__)

reddit = praw.Reddit(user_agent=settings.REDDIT_USER_AGENT)
reddit.login(username=settings.REDDIT_USERNAME,
             password=settings.REDDIT_PASSWORD)
search_subreddits = (
    'politics',
    # 'funny',
    # 'gaming',
    # 'atheism',
    # 'trees',
    # 'starcraft',
    # 'anime'
)

@periodic_task(run_every=crontab(minute="*/2"))
def search_subreddits_for_trolls():
    """
    Crawl the subreddits for trolls
    """
    logger.info("Starting reddit troll search")
    for subreddit in search_subreddits:
        submissions = reddit.get_subreddit(subreddit).get_hot(limit=15)
        logger.info("Searching submissions in '%s'" % subreddit)
        for submission in submissions:
            logger.info("Searching comments in '%s'" % submission.title)
            comments = submission.comments_flat
            for comment in comments:
                if hasattr(comment, 'body') and troll_classifier.it_is_a_troll(
                    troll_model, feature_words, comment.body):
                    logger.info("Troll detected! Saving %s to db." % comment.id)
                    new_sub, new_com = save_submission_and_comment(submission, comment)
                    if new_sub:
                        logger.info("New submission '%s' saved" % submission.title)
                    if new_com:
                        logger.info("New troll comment '%s' saved" % comment.id)

    logger.info("Troll search completed")
