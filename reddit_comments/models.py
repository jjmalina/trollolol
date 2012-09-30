from mogo import Model, Field, connect, ReferenceField

import settings

connect(settings.MONGO_DB_NAME, host=settings.MONGO_HOST, port=settings.MONGO_PORT)


class Submission(Model):
    id = Field(unicode, required=True)
    title = Field(unicode, required=True)
    permalink = Field(unicode, required=True)
    url = Field(unicode, required=True)


class Comment(Model):
    replied_to = Field(bool, default=False)
    id = Field(unicode, required=True)
    author_id = Field(unicode, required=True)
    author_name = Field(unicode, required=True)
    body = Field(unicode, required=True)
    body_html = Field(unicode, required=True)
    permalink = Field(unicode, required=True)
    submission = ReferenceField(Submission)


class TrollClassifierWeights(Model):
    id = Field(int, required=True)
    data = Field(unicode)