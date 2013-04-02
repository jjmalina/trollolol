import simplejson as json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from reddit_comments.models import Submission, Comment


def index(request):
    submissions = []
    for submission in Submission.find():
        item = {'submission': submission, 'comments': []}
        for comment in submission.comments:
            item['comments'].append(comment)
        submissions.append(item)
    context = {'submissions': submissions}
    return render(request, 'reddit_comments/index.html', context)


@csrf_exempt
def classify_comment(request):
    """Ajax view when the user classifies the comment themself"""
    data = json.loads(request.POST['classify'])
    label = data['label']
    object_id = data['objectId']
    comment = Comment.find_one({'object_id': object_id})
    comment.is_troll = label
    comment.is_classified = True
    comment.save()
    response = {
        'status': 'success',
        'label': label,
        'objectId': object_id
    }
    return HttpResponse(json.dumps(response))