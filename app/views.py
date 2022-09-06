from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from app.models import Message
from .forms import CustomUsercreationForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User




# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    return render(request, 'apps/index.html', {})

def register(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    form = CustomUsercreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('app:login')
    context = {"form": form}
    return render(request, 'apps/register.html', context)

@login_required
def home(request):
    users = User.objects.exclude(username = request.user.username)
    paginator = Paginator(users, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'users' : page_obj
    }
    return render(request, 'apps/home.html', context)

@login_required
def chat(request, username):
    msg_receiver = User.objects.get(username = username)
    form = MessageForm(request.POST or None)
    context = {
        "form": form,
        "receiver": msg_receiver,
        "sender": request.user
    }
    # if form.is_valid():
    #     msg = form.cleaned_data['msg']
    #     msg_obj = Message.objects.create(msg_sender = request.user, msg_receiver = msg_receiver, msg = msg)
    #     msg_obj.save()
    #     context['form'] = MessageForm()
    return render(request, 'apps/chat.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('app:home')
    else:
        form = AuthenticationForm(request)
    context = {
        "form": form
    }
    return render(request, 'apps/login.html', context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("app:login")
    return render(request, "apps/logout.html", {})