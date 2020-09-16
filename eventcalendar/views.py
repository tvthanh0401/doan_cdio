from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from calendarapp.forms import SignupForm
from django.contrib import messages

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            result = User.objects.filter(email=form.cleaned_data.get('email'))
            if result:
                messages.error(request, 'This email is already used by another user.')
            else:
                form.save()
                messages.success(request, 'Your account is created, please login now.')
                return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        username = request.POST.get('username')
        passwd = request.POST.get('password')
        user = authenticate(request, username=username, password=passwd)
        if user:
            login(request, user)
            return redirect('calendarapp:calendar')
        else:
            messages.info(request, 'Username or password is incorect')
    context = {}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')