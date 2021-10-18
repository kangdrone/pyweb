from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from poll.models import Question

def poll_index(request):
    question_list = Question.objects.all()
    context = {'question_list': question_list}
    return render(request, 'poll/poll_index.html', context)

def poll_detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'poll/poll_detail.html', context)
    # return HttpResponse("You are looking at question %s." % question_id)

# 127.0.0.1:8000/poll/2/vote
def vote(request, question_id):
    try:
        # question = Question.objects.get(id=question_id)
        question = get_object_or_404(Question, pk=question_id)
        choice = request.POST['choice']   # name에서 가져오기
        sel_choice = question.choice_set.get(id=choice)
    except KeyError:
        return render(request, 'poll/poll_detail.html', {
            'question': question,
            'error_message': '항목을 선택을 해주십시오.'
        })
    else:
        sel_choice.votes += 1
        sel_choice.save()
        return HttpResponseRedirect(reverse('poll:result', args=(question.id,)))

# 127.0.0.1:8000/poll/result/2/result
def result(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'poll/result.html', context)

