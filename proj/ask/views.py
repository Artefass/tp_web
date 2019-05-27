from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Count

from .models import (
    Question, Answer, Tag, Vote, Profile
)

# Create your views here.

def userdata():
    user = {
        "id": 1,
        "email": "example@com",
        "login": "qwerty",
        "nickname": "Dr.House"
    }
    return user


def paginate(objects_list, request):
    page_num  = request.GET.get("page", "1")
    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1

    page_size = request.GET.get("page_size", "5")
    try:
        page_size = int(page_size)
        page_size = page_size if page_size >= 5 and page_size <= 10 else 5
    except ValueError:
        page_size = 5

    paginator = Paginator(objects_list, page_size)

    try:
        page = paginator.get_page(page_num)
    except InvalidPage:
        page = paginator.get_page(1)

    return page, paginator

@require_GET
def index(request):
    questions = Question.objects.new()
    questions_page, _ = paginate(questions, request)
    questions_page.object_list = questions_page.object_list.annotate(answers_count=Count('answer'))
    search_type = "new"

    context = {
        "questions_page": questions_page,
        "search_type": search_type,
    }

    return render(request, 'ask/index_new.html', context=context)

@require_GET
def index_hot(request):
    questions = Question.objects.hot()
    questions_page, _ = paginate(questions, request)
    questions_page.object_list = questions_page.object_list.annotate(answers_count=Count('answer'))
    search_type = "hot"

    context = {
        "questions": questions_page.object_list,
        "questions_page": questions_page,
        "search_type": search_type
    }
    return render(request, 'ask/index_hot.html', context=context)

@require_GET
def index_search_by_tag(request, tag_name):
    questions = Question.objects.filter(tags__name=tag_name)
    questions_page, _ = paginate(questions, request)
    questions_page.object_list = questions_page.object_list.annotate(answers_count=Count('answer'))

    context = {
        "questions_page": questions_page,
        "tag_name": tag_name
    }
    return render(request, 'ask/index_search_by_tag.html', context=context)

def ask(request):
    return render(request, 'ask/ask.html')

def login(request):
    return render(request, 'ask/login.html')

def signup(request):
    return render(request, 'ask/signup.html')

@require_GET
def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers  = Answer.objects.filter(question_id=question_id)
    answers_page, _ = paginate(answers, request)

    context = {
        "question" : question,
        "answers_page": answers_page,
    }

    return render(request, 'ask/question.html', context=context)

def settings(request):
    user = userdata()

    context = {
        "user":user
    }
    return render(request, 'ask/settings.html', context=context)