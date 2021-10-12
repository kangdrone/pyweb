from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from pybo.models import Question
from pybo.forms import QuestionForm


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

# 질문 등록
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)   # 임시저장
            question.create_date = timezone.now()   # 등록일
            question.save()   # 실제 저장
            return redirect('pybo:index')
    else:   # request.method == 'GET':
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)