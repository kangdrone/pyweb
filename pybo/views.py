from django.http import HttpResponse
from django.shortcuts import render

from pybo.models import Question


def index(request):
    # return HttpResponse("Welcome Mysite!")
    question_list = Question.objects.all()
    content = {'question_list':question_list}
    return render(request, 'pybo/question_list.html', content)

# 상세 페이지 조회
def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    cotext = {'question':question}
    return render(request, 'pybo/detail.html', cotext)