from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from ...models import (
    Question, Answer, Tag, Vote, Profile
)
import random

class Command(BaseCommand):
    help = 'Generate data for models Question, Answer, Vote, Profile, Tag'

    def handle(self, *args, **options):
        # очистка таблиц
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Tag.objects.all().delete()
        Vote.objects.all().delete()
        Profile.objects.all().delete()

        MAX_RANDOM_USER = 10
        MAX_RANDOM_TAGS = 20
        MAX_RANDOM_QUESTIONS = 30
        MAX_RANDOM_ANSWERS = 40
        MAX_RANDOM_VOTES = 20


        # генерируем теги
        for i in range(1, MAX_RANDOM_TAGS + 1):
            tag = Tag(id = i, name="tag-text-{}".format(i))
            tag.save()

        # генерируем пользователей
        for i in range(1, MAX_RANDOM_USER + 1):
            email = "example.{}@mail.ru".format(i)
            username = "username-{}".format(i)
            password = "123Paul-{}".format(i)
            user = User(
                id=i,
                username=username,
                email=email
            )
            user.set_password(password)
            user.save()

        # генерируем профили
        for i in range(1, MAX_RANDOM_USER + 1):
            nickname = "nickname-{}".format(i)
            profile = Profile(
                id=i,
                user=User.objects.get(id=i),
                nickname=nickname)
            profile.save()

        # генерируем вопросы
        for i in range(1, MAX_RANDOM_QUESTIONS + 1):
            title = "Две фазы в выключателе без нагрузки ---- {}".format(i)
            description = "При установке нового димера замерил " \
                           "пробником-отверткой два провода на выключатель" \
                           " - и там и там фаза! Как?! Лампы в люстре " \
                           "выкручены все. Вкрутили лампу, на выключателе,"\
                           " как и положено - ноль и фаза, лампа светит"\
                           " при замыкании контактов на выключатель."\
                           " Выкручиваем лампу - опять вторая фаза "\
                           "появляется. Замыкание между проводов нет,"\
                           " проверял мультиметром. На люстре - фаза"\
                           " на постоянке, пробник показывает. И "\
                           "одновременно фаза на обоих концах провода"\
                           " на выключатель. Что за ерунда...."

            random_user = random.randint(1, MAX_RANDOM_USER)
            random_tags_id_list = list(range(1,MAX_RANDOM_TAGS + 1))
            random.shuffle(random_tags_id_list)
            random_tags_list = list([Tag.objects.get(id=j) for j in random_tags_id_list[:4]])
            question = Question(
                id=i,
                title=title,
                description=description,
                user=User.objects.get(id=random_user))
            question.save()
            question.tags.set(random_tags_list)

        # генерируем ответы
        for i in range(1, MAX_RANDOM_ANSWERS + 1):
            random_question = random.randint(1, MAX_RANDOM_QUESTIONS)
            random_user = random.randint(1, MAX_RANDOM_USER)
            text = "предположим, что чудес не бывает, тогда " \
                "предположение 1- диммер не все равно как "\
                "его подключать, т.е фаза к фазе. N к N. это"\
                " надо проверить в описании и на клеммах. "\
                "предположение 2 - 1 диммер сгорел. второй "\
                "неисправен. легко проверить на лампочке с "\
                "'настольной' проводкой."

            correct = random.randint(0,1)
            correct = True if correct else False

            question = Question.objects.get(id=random_question)
            question.answers_count += 1
            question.save()
            answer = Answer(
                id=i,
                question=question,
                text=text,
                user=User.objects.get(id=random_user),
                correct=correct
            )
            answer.save()

        # генерируем голоса
        for i in range(1, MAX_RANDOM_VOTES + 1):
            random_user = random.randint(1, MAX_RANDOM_USER)
            content_type_list = [
                ContentType.objects.get_for_model(Question),
                ContentType.objects.get_for_model(Answer),
            ]

            random_vote = random.randint(0,1)
            random_vote = 1 if random_vote else -1

            random_content_type = random.randint(0,1)
            random_content_type = content_type_list[random_content_type]

            if random_content_type == content_type_list[0]:
                object_id = random.randint(1, MAX_RANDOM_QUESTIONS)
            else:
                object_id = random.randint(1, MAX_RANDOM_ANSWERS)

            vote = Vote(
                id=i,
                user_vote=random_vote,
                user=User.objects.get(id=random_user),
                content_type=random_content_type,
                object_id=object_id
            )
            vote.save()

        self.stdout.write("Generation data is success!")


