from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, InvalidPage

# Create your views here.

# test data
def questionsdata():
    questions = [{
            "id": i,
            "name":"Две фазы в выключателе без нагрузки",
            "description": "При установке нового димера замерил " +
                           "пробником-отверткой два провода на выключатель" +
                           " - и там и там фаза! Как?! Лампы в люстре "
                           "выкручены все. Вкрутили лампу, на выключателе,"
                           " как и положено - ноль и фаза, лампа светит"
                           " при замыкании контактов на выключатель."
                           " Выкручиваем лампу - опять вторая фаза "
                           "появляется. Замыкание между проводов нет,"
                           " проверял мультиметром. На люстре - фаза"
                           " на постоянке, пробник показывает. И "
                           "одновременно фаза на обоих концах провода"
                           " на выключатель. Что за ерунда....",
            "tags": ["Проводка", "фазы", "электропитание"],
            "raiting":123,
            "count_answers": 3
    } for i in range(1,40)]
    return list(questions)

def answersdata(question_id = 1):
    answers = [{
        "id": i,
        "question_id": question_id,
        "text": "предположим, что чудес не бывает, тогда "
                "предположение 1- диммер не все равно как "
                "его подключать, т.е фаза к фазе. N к N. это"
                " надо проверить в описании и на клеммах. "
                "предположение 2 - 1 диммер сгорел. второй "
                "неисправен. легко проверить на лампочке с "
                "'настольной' проводкой.",
        "correct": True,
        "raiting": 10,
    } for i in range(1,10)]
    return list(answers)

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
    questions = questionsdata()
    questions_page, questions_paginator = paginate(questions, request)
    search_type = "new"

    auth = request.GET.get("auth")
    print(auth)
    user = {}
    if auth:
        user.update(userdata())

    context = {
        "questions": questions_page.object_list,
        "questions_page": questions_page,
        "paginator": questions_paginator,
        "user":user,
        "search_type": search_type
    }

    return render(request, 'ask/index_new.html', context=context)

@require_GET
def index_hot(request):
    questions = questionsdata()
    questions_page, questions_paginator = paginate(questions, request)
    search_type = "hot"

    auth = request.GET.get("auth")
    user = {}
    if auth:
        user.update(userdata())

    context = {
        "questions": questions_page.object_list,
        "questions_page": questions_page,
        "paginator": questions_paginator,
        "user": user,
        "search_type": search_type
    }
    return render(request, 'ask/index_hot.html', context=context)

@require_GET
def index_search_by_tag(request, tag_name):
    questions = questionsdata()
    questions_page, questions_paginator = paginate(questions, request)

    user = {}

    context = {
        "questions": questions_page.object_list,
        "questions_page": questions_page,
        "paginator": questions_paginator,
        "user": user,
        "tag_name": tag_name
    }
    return render(request, 'ask/index_search_by_tag.html', context=context)

def ask(request):
    return render(request, 'ask/ask.html')

def login(request):
    return render(request, 'ask/login.html')

def signup(request):
    return render(request, 'ask/signup.html')

def question(request, question_id):
    question = questionsdata()[question_id - 1]
    answers  = answersdata(question_id)
    answers[1]["correct"] = False

    answers_page, answers_paginator = paginate(answers, request)

    context = {
        "question" : question,
        "answers": answers_page.object_list,
        "answers_page": answers_page,
        "answers_paginator": answers_paginator,
    }
    return render(request, 'ask/question.html', context=context)

def settings(request):
    user = userdata()

    context = {
        "user":user
    }
    return render(request, 'ask/settings.html', context=context)