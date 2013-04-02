from mogo import Model, Field, connect, ReferenceField

from reddit_comments import troll_classifier

import sys
import time
import settings
import logging
logger = logging.getLogger(__name__)
connect(settings.MONGO_DB_NAME, host=settings.MONGO_HOST, port=settings.MONGO_PORT)


class Submission(Model):
    object_id = Field(unicode, required=True)
    title = Field(unicode, required=True)
    permalink = Field(unicode, required=True)
    url = Field(unicode, required=True)
    date_added = Field(int, required=True)

    @property
    def comments(self):
        return Comment.search(submission=self, is_classified=False)

    @property
    def troll_count(self):
        total_comments = Comment.search(submission=self).count()
        not_trolls = Comment.search(submission=self, is_classified=True, is_troll=False).count()
        return total_comments - not_trolls


class Comment(Model):
    replied_to = Field(bool, default=False)
    is_troll = Field(bool, default=False)
    is_classified = Field(bool, default=False)
    object_id = Field(unicode, required=True)
    author_id = Field(unicode, required=True)
    author_name = Field(unicode, required=True)
    body = Field(unicode, required=True)
    body_html = Field(unicode, required=True)
    permalink = Field(unicode, required=True)
    submission = ReferenceField(Submission)
    date_added = Field(int, required=True)


def save_submission_and_comment(r_submission, r_comment):
    submission = Submission.find_one({'object_id': r_submission.id})
    new_sub = False if submission is not None else True
    submission = Submission(
        object_id=r_submission.id,
        title=r_submission.title,
        permalink=r_submission.permalink,
        url=r_submission.url,
        date_added=int(time.time())
    ) if new_sub else submission
    submission.save()

    comment = Comment.find_one({'object_id': r_comment.id})
    new_com = False if comment is not None else True
    Comment(
        object_id=r_comment.id,
        author_id=r_comment.author.id,
        author_name=r_comment.author.name,
        body=r_comment.body,
        body_html=r_comment.body_html,
        permalink=r_comment.permalink,
        submission=submission,
        date_added=int(time.time())
    ).save() if new_com else comment
    return new_sub, new_com

# we train the classifier on server start
logger.info("Starting classification model training.")
# troll_model, feature_words = troll_classifier.load_troll_classification_model()
logger.info("Starting classification model training finished.")
