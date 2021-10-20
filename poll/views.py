from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from poll.models import Question, Choice

# 설문 목록
def poll_list(request):
    question_list = Question.objects.all()
    context = {'question_list': question_list}
    return render(request, 'poll/poll_list.html', context)

# 설문 상세
def poll_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'poll/poll_detail.html', context)

# 투표하기
def vote(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
        choice = request.POST['choice']  # name에서 가져오기
        sel_choice = question.choice_set.get(id=choice)
    except KeyError:
        return render(request, 'poll/poll_detail.html', {
            'question': question,
            'error_message': '항목을 선택 해주세요'
        })
    else:
        sel_choice.votes += 1
        sel_choice.save()
        return HttpResponseRedirect(reverse('poll:result', args=(question.id,)))

# 투표 결과
def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'poll/result.html', context)


