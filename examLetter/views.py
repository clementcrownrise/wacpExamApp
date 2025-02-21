from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import SignupForm, LoginForm



def home(request):
    return redirect('/accounts/login')
  


#def login(request):
#    return HttpResponse("login form will be here")

def logout_view(request):
    logout(request)
    return redirect('/accounts/login')


def user_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")  
            return redirect('examination:index')
    else:
        form = LoginForm()
    return render(request, 'examLetter/login.html',{'LoginForm':LoginForm})



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'examLetter/signup.html',{'form':form})