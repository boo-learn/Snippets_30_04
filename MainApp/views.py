from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib import auth
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet(request):
    if request.method == "GET":  # получить страницу с формой
        form = SnippetForm()
        context = {
            'form': form,
            'pagename': 'Добавление нового сниппета'
        }
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == "POST":  # получить данные от формы
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
        return redirect('snippets-list')


# 127.0.0.1:8000/snippets/list?sort=name
def snippets_page(request):
    snippets = Snippet.objects.all()
    sort = request.GET.get('sort')
    lang = request.GET.get("lang")
    if sort:
        snippets = snippets.order_by(sort)
    if lang:
        snippets = snippets.filter(lang=lang)
    users = User.objects.annotate(num_snippets=Count('snippets')).exclude(num_snippets=0)
    context = {
        'pagename': 'Просмотр сниппетов',
        "snippets": snippets,
        "sort": sort,
        "lang": lang,
        "users": users
    }
    return render(request, 'pages/view_snippets.html', context)


@login_required
def snippets_my(request):
    my_snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        "snippets": my_snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    comment_form = CommentForm()
    context = {
        'pagename': 'Информация о сниппете',
        "snippet": snippet,
        "comment_form": comment_form
    }
    return render(request, 'pages/snippet-detail.html', context)


def snippet_delete(requests, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    if snippet.user != requests.user:
        raise PermissionDenied()
    snippet.delete()
    return redirect('snippets-list')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
    return redirect('home')


def logout_page(request):
    auth.logout(request)
    return redirect('home')


def registration(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {
            'pagename': 'Регистрация',
            "form": form
        }
        return render(request, 'pages/registration.html', context)
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        else:  # данные не валидные
            context = {
                'pagename': 'Регистрация',
                "form": form
            }
            return render(request, 'pages/registration.html', context)
        return redirect('home')


def comment_create(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snippet_id = request.POST.get("snippet_id")
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            snippet = Snippet.objects.get(id=snippet_id)
            comment.snippet = snippet
            comment.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
