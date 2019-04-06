from django.shortcuts import render

# Create your views here.

# test data
def questiondata():
    question = {
            "id": 1,
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
    }
    return question

def answerdata():
    answer = {
        "id": 1,
        "text": "предположим, что чудес не бывает, тогда "
                "предположение 1- диммер не все равно как "
                "его подключать, т.е фаза к фазе. N к N. это"
                " надо проверить в описании и на клеммах. "
                "предположение 2 - 1 диммер сгорел. второй "
                "неисправен. легко проверить на лампочке с "
                "'настольной' проводкой.",
        "correct": True,
        "raiting": 10,
    }
    return answer

def index(request, tag = None):
    auth = request.GET.get("auth")
    print(auth)
    user = {}
    if auth:
        user["nickname"] = "Dr.House"
        print("OK")
    question = questiondata()
    questions = [question] * 2

    context = {
        "questions": questions,
        "user":user
    }

    search_type = request.GET.get("search_type", "new")
    if search_type == "question":
        context.update({"question": "Бла бла бла"})
    elif tag is not None:
        context.update({"tag_name": tag})
        search_type = "tag"

    context["search_type"] = search_type

    return render(request, 'ask/index.html', context=context)

def ask(request):
    return render(request, 'ask/ask.html')

def login(request):
    return render(request, 'ask/login.html')

def signup(request):
    return render(request, 'ask/signup.html')

def question(request, question_id):

    question = questiondata()
    answer  = answerdata()
    answers = [answer.copy() for i in range(3)]
    answers[1]["correct"] = False

    return render(request, 'ask/question.html', context={
        "question": question,
        "answers":  answers
    })

def settings(request):
    user = {
        "id": 1,
        "email": "example@com",
        "login": "qwerty",
        "nickname": "Dr.House"
    }
    return render(request, 'ask/settings.html', context={
        "user": user
    })