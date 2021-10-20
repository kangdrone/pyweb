from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from common.forms import UserForm

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  #회원 저장
            # 가입과 동시에 자동로그인
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password1) #user 객체 생성
            login(request, user)   #로그인한 사용자(세션이 발급된 user)
            return redirect('pybo:index')
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'common/signup.html', context)