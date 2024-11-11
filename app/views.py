from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Question, Answer, Tag

# Пагинация
def paginate(objects_list, request, per_page):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page

# Отображение главной страницы с новыми вопросами
def index(request):
    questions = Question.objects.best_questions()
    tags = Tag.objects.all()  # получение всех тегов для отображения
    page = paginate(questions, request, 5)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page': page, 'tags': tags},
    )

# Страница входа
def login(request):
    tags = Tag.objects.all()
    return render(request, 'login.html', {'tags': tags})

#Отображение страницы конкретного вопроса
def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)  # получение вопроса по id
    answers = Answer.objects.filter(question=question)  # получение ответов, связанных с вопросом
    page = paginate(answers, request, 5)
    tags = Tag.objects.all()
    return render(
        request, 'question.html',
        {'question': question, 'answers': page.object_list, 'page': page, 'tags': tags},
    )

# Страница настроек
def settings(request):
    tags = Tag.objects.all()
    return render(request, 'settings.html', {'tags': tags})

# Страница регистрации
def signup(request):
    tags = Tag.objects.all()
    return render(request, 'signup.html', {'tags': tags})

# Страница для публикации нового вопроса
def ask(request):
    tags = Tag.objects.all()
    return render(request, 'ask.html', {'tags': tags})

# Базовая страница пользователя
def base_user(request):
    tags = Tag.objects.all()
    return render(request, 'layouts/base_user.html', {'tags': tags})

# Отображение вопросов по тегу
def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.filter(tags=tag)  # вопросы, связанные с этим тегом
    page = paginate(questions, request, 5)
    tags = Tag.objects.all()
    return render(
        request, 'tag.html',
        {'tag': tag, 'questions': page.object_list, 'page': page, 'tags': tags},
    )

# Отображение новых вопросов
def new_questions(request):
    questions = Question.objects.new_questions()
    page = paginate(questions, request, 5)
    tags = Tag.objects.all()
    return render(request, 'ask.html', {'questions': page, 'tags': tags})

# Отображение популярных вопросов
def hot(request):
    questions = Question.objects.best_questions()
    tags = Tag.objects.all()  # получение всех тегов для отображения
    page = paginate(questions, request, 5)
    return render(
        request, 'hot.html',
        context={'questions': page.object_list, 'page': page, 'tags': tags},
    )