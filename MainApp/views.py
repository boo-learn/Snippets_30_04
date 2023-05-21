from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import auth
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm


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


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        "snippets": snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    context = {
        'pagename': 'Информация о сниппете',
        "snippet": snippet
    }
    return render(request, 'pages/snippet-detail.html', context)


def snippet_delete(requests, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
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