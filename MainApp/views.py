from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    form = SnippetForm()
    context = {
        'form': form,
        'pagename': 'Добавление нового сниппета'
    }
    return render(request, 'pages/add_snippet.html', context)


# Получаем данные формы --> Создаем Сниппет
def snippet_create(request):
    if request.method == "POST":
        # form_data = request.POST
        # snippet = Snippet(
        #     name=form_data['name'],
        #     lang=form_data['lang'],
        #     code=form_data['code'],
        # )
        # snippet.save()
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
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
