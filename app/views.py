import copy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
# Create your views here.


questions = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'Text of question {i}?',
        'tagsName': ["one", "two", "three"],
    } for i in range(30)
]

answers = [
    {
        'user_id': i+5,
        'text': f'Text of asnwer {i}'
    } for i in range(10)
]

tags = [
    {
        'text': 'one',
    },
    {
        'text': 'two',
    },
    {
        'text': 'three',
    },
    {
        'text': 'four',
    },
    {
        'text': 'five',
    },
    {
        'text': 'six',
    },
    {
        'text': 'seven',
    },
    {
        'text': 'eight',
    }
]


def paginate(objects_list, request, per_page):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # Если параметр `page` не является числом, возвращаем первую страницу
        page = paginator.page(1)
    except EmptyPage:
        # Если запрашиваемая страница выходит за пределы, возвращаем последнюю страницу
        page = paginator.page(paginator.num_pages)

    return page


def index(request):
    page = paginate(questions, request, 5)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page': page, 'tags': tags},
    )

def hot(request):

    page = paginate(questions, request, 5)
    return render(
        request, 'hot.html',
        context={'questions': page.object_list, 'page': page, 'tags': tags},
    )

def login(request):

    return render(
        request, 'login.html', {'tags': tags}
    )

def question(request, question_id):
    question = questions[question_id]
    page = paginate(answers, request, 5)
    return render(
        request, 'question.html',
        {'question': question, 'answers': page.object_list, 'page': page, 'tags': tags},
    )

def settings(request):
    return render(
        request, 'settings.html', {'tags': tags}
        )

def signup(request):
    return render(
        request, 'signup.html',{'tags': tags}
        )

def ask(request):
    return render(
        request, 'ask.html', {'tags': tags}
        )

def base_user(request):
    return render(
        request, 'layouts/base_user.html', {'tags': tags}
        )

def tag(request, tag_name):
    # Найдём тег с text, равным tag_name
    tag_item = next((tag for tag in tags if tag['text'] == tag_name), None)
    if not tag_item:
        # Если тег не найден, можно вернуть 404
        return render(request, '404.html', status=404)

    page = paginate(questions, request, 5)
    return render(
        request, 'tag.html',
        {'tag': tag_item, 'questions': page.object_list, 'page': page, 'tags': tags},
    )