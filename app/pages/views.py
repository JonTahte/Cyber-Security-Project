from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.db import connection
from django.utils import timezone
from .models import Comment

# Create your views here.


def homePageView(request):
    try:
        comments = Comment.objects.order_by('pub_time')
    except:
        comments = None
    return render(request, 'pages/index.html', {'comments' : comments})


@login_required
# # delete next row
@csrf_exempt
def add(request):
    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        if comment:
            Comment.objects.create(owner=request.user, comment=comment)
    return redirect('/')

@login_required
def delete(request):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=request.POST.get('id'))
        # if request.user == comment.owner:
        #     comment.delete()
        comment.delete()
    return redirect('/')


def profileView(request, user_id):
    # target = User.objects.filter(id=user_id).first()
    target_list = list(User.objects.raw(f"SELECT * FROM auth_user WHERE id={user_id}"))
    target = target_list[0] if len(target_list) > 0 else None
    if not target:
        return redirect('/')
    else:
        comments = Comment.objects.filter(owner=target).order_by('pub_time')
        return render(request, 'pages/profile.html', {'target': target, 'comments': comments})

def registerView(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "pages/register.html")

def create_account(request):
    if request.method == 'GET':
        return redirect('register')
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        try:
            # User.objects.create_user(username=username, password=password1)
            user = User(username = username)
            user.password = password1
            user.save()
        except IntegrityError:
            messages.error(request, 'Username is already in use')
            return redirect('register')

        messages.info(request, 'Account created successfully')
    return redirect('/login')

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # user = authenticate(request, username=username, password=password)
        user = User.objects.filter(username=username).first()
        if user is not None:
            # # delete next if statement and fix the indentation
            if user.password == password:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Username and password do not match')
        else:
            messages.error(request, 'Username and password do not match')
    else:
        if request.user.is_authenticated:
            logout(request)
    return render(request, 'pages/login.html')
