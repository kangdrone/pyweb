from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from pybo.models import Question
from pybo.forms import QuestionForm, AnswerForm

def index(request):
    return render(request, 'pybo/index.html')

# 전체 목록 조회
def board(request):
    #페이지 - #127.0.0.1:8000/pybo/?page=1
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    #조회
    question_list = Question.objects.order_by('-create_date') #내림차순 정렬
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  #제목 검색
            Q(content__icontains=kw) |  #질문내용 검색
            Q(answer__content__icontains=kw) |  # 답변내용 검색
            Q(author__username__icontains=kw) |  #질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  #답변 글쓴이
        ).distinct()   # 중복 제거한 유일한 내용

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw} #page, kw 추가
    return render(request, 'pybo/question_list.html', context)

# 상세 페이지 조회
def detail(request, question_id):
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    cotext = {'question': question}
    return render(request, 'pybo/detail.html', cotext)

# 질문 등록
@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)  # 임시 저장
            question.author = request.user  # 세션 권한이 있는 user(author)
            question.create_date = timezone.now() # 등록일
            question.save()  # 실제 저장
            return redirect('pybo:board')
    else:  # request.method == 'GET':
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

# 답변 등록
@login_required(login_url='common:login')
def answer_create(request, question_id):
    #question = Question.objects.get(id=question_id)  #질문 1개 가져오기
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question  # 질문을 답변에 저장(외래키)
            form.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'form': form}
    return render(request, 'pybo:detail', context)

#질문 수정
@login_required(login_url='common:login')
def question_modify(request, question_id):
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user   #세션권한이 있는 user 생성
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)  #기존의 내용을 가져옴(question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

#질문 삭제
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect('pybo:index')