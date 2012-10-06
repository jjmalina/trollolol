from django.shortcuts import render

from reddit_comments.models import Submission, Comment

def index(request):
    comment = Comment.find_one()
    context = {'comment': comment}
    return render(request, 'reddit_comments/index.html', context)