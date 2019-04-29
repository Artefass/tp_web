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
        MAX_RANDOM_USER = 500
        MAX_RANDOM_TAGS = 10000
        MAX_RANDOM_QUESTIONS = 1000
        MAX_RANDOM_ANSWERS = 10000
        MAX_RANDOM_VOTES = 20000

        CHUNK_SIZE = 200

        max_delete_in_iteration = 900

        # очистка таблиц
        # Profile.objects.all().delete()
        while Profile.objects.count():
            profiles_ids = Profile.objects.all().values("pk")[:max_delete_in_iteration]
            profiles = Profile.objects.filter(pk__in=profiles_ids)
            profiles.delete()

        # Tag.objects.all().delete()
        while Tag.objects.count():
            tags_ids = Tag.objects.all().values("pk")[:max_delete_in_iteration]
            tags = Tag.objects.filter(pk__in=tags_ids)
            tags.delete()

        # Vote.objects.all().delete()
        while Vote.objects.count():
            votes_ids = Vote.objects.all().values("pk")[:max_delete_in_iteration]
            votes = Vote.objects.filter(pk__in=votes_ids)
            votes.delete()

        # Answer.objects.all().delete()
        while Answer.objects.count():
            answers_ids = Answer.objects.all().values("pk")[:max_delete_in_iteration]
            answers     = Answer.objects.filter(pk__in=answers_ids)
            answers.delete()

        # Question.objects.all().delete()
        while Question.objects.count():
            questions_ids = Question.objects.all().values("pk")[:max_delete_in_iteration]
            questions     = Question.objects.filter(pk__in=questions_ids)
            questions.delete()

        # max_del_id = MAX_RANDOM_USER - 100
        while User.objects.count():
            # User.objects.filter(pk__gt=max_del_id).delete()
            # max_del_id -= 100
            users_ids = User.objects.values_list('pk', flat=True)[:max_delete_in_iteration]
            users = User.objects.filter(pk__in=users_ids)
            users.delete()

        # генерируем теги

        tags_count = 0
        while tags_count < MAX_RANDOM_TAGS:
            chunk = CHUNK_SIZE if MAX_RANDOM_TAGS - tags_count > CHUNK_SIZE else MAX_RANDOM_TAGS - tags_count
            tags_objs_list = []
            for i in range(tags_count + 1, tags_count + chunk + 1):
                tag = Tag(id=i, name="tag-text-{}".format(i))
                tags_objs_list.append(tag)
            Tag.objects.bulk_create(tags_objs_list)
            tags_count += chunk

        self.stdout.write("Generation Tags is success!")

        # генерируем пользователей
        users_count = 0
        while users_count < MAX_RANDOM_USER:
            chunk = CHUNK_SIZE if MAX_RANDOM_USER - users_count > CHUNK_SIZE else MAX_RANDOM_USER - users_count
            users_objs_list = []
            for i in range(users_count + 1, users_count + chunk + 1):
                email = "example.{}@mail.ru".format(i)
                username = "username-{}".format(i)
                password = "123Paul-{}".format(i)
                user = User(
                    id=i,
                    username=username,
                    email=email
                )
                user.set_password(password)
                users_objs_list.append(user)
            User.objects.bulk_create(users_objs_list)
            users_count += chunk

        self.stdout.write("Generation Users is success!")

        # генерируем профили
        profiles_count = 0
        while profiles_count < MAX_RANDOM_USER:
            chunk = CHUNK_SIZE if MAX_RANDOM_USER - profiles_count > CHUNK_SIZE else MAX_RANDOM_USER - profiles_count
            profiles_objs_list = []
            for i in range(profiles_count + 1, profiles_count + chunk + 1):
                nickname = "nickname-{}".format(i)
                profile = Profile(
                    id=i,
                    user_id=i,
                    nickname=nickname
                )
                profiles_objs_list.append(profile)
            Profile.objects.bulk_create(profiles_objs_list)
            profiles_count += chunk

        self.stdout.write("Generation User's Profile is success!")

        # генерируем вопросы
        questions_count = 0
        while questions_count < MAX_RANDOM_QUESTIONS:
            chunk = CHUNK_SIZE if MAX_RANDOM_QUESTIONS - questions_count > CHUNK_SIZE else MAX_RANDOM_QUESTIONS - questions_count
            questions_objs_list = []
            for i in range(questions_count + 1, questions_count + chunk + 1):
                title = "Две фазы в выключателе без нагрузки ---- {}".format(i)
                description = "При установке нового димера замерил " \
                              "пробником-отверткой два провода на выключатель" \
                              " - и там и там фаза! Как?! Лампы в люстре " \
                              "выкручены все. Вкрутили лампу, на выключателе," \
                              " как и положено - ноль и фаза, лампа светит" \
                              " при замыкании контактов на выключатель." \
                              " Выкручиваем лампу - опять вторая фаза " \
                              "появляется. Замыкание между проводов нет," \
                              " проверял мультиметром. На люстре - фаза" \
                              " на постоянке, пробник показывает. И " \
                              "одновременно фаза на обоих концах провода" \
                              " на выключатель. Что за ерунда...."
                random_user = random.randint(1, MAX_RANDOM_USER)
                question = Question(
                    id=i,
                    title=title,
                    description=description,
                    user_id=random_user
                )
                questions_objs_list.append(question)
            Question.objects.bulk_create(questions_objs_list)
            questions_count += chunk
            print(questions_count)

        for i in range(1, MAX_RANDOM_QUESTIONS + 1):
            random_tags_ids_list = []
            for j in range(4):
                tag_id = random.randint(1, MAX_RANDOM_TAGS)
                while tag_id in random_tags_ids_list:
                    tag_id = random.randint(1, MAX_RANDOM_TAGS)
                random_tags_ids_list.append(tag_id)
            question = Question.objects.get(id=i)
            question.tags.set(random_tags_ids_list)

        self.stdout.write("Generation Questions is success!")

        # генерируем ответы
        answers_count = 0
        while answers_count < MAX_RANDOM_ANSWERS:
            chunk = CHUNK_SIZE if MAX_RANDOM_ANSWERS - answers_count > CHUNK_SIZE else MAX_RANDOM_ANSWERS - answers_count
            answers_objs_list = []
            for i in range(answers_count + 1, answers_count + chunk + 1):
                random_question_id = random.randint(1, MAX_RANDOM_QUESTIONS)
                random_user_id = random.randint(1, MAX_RANDOM_USER)
                text = "предположим, что чудес не бывает, тогда " \
                       "предположение 1- диммер не все равно как " \
                       "его подключать, т.е фаза к фазе. N к N. это" \
                       " надо проверить в описании и на клеммах. " \
                       "предположение 2 - 1 диммер сгорел. второй " \
                       "неисправен. легко проверить на лампочке с " \
                       "'настольной' проводкой."
                correct = random.randint(0, 1)
                correct = True if correct else False
                answer = Answer(
                    id=i,
                    question_id=random_question_id,
                    text=text,
                    user_id=random_user_id,
                    correct=correct
                )
                answers_objs_list.append(answer)
            Answer.objects.bulk_create(answers_objs_list)
            answers_count += chunk

        self.stdout.write("Generation Answers is success!")

        # генерируем голоса
        vote_setting = {
            "question": {
                "model": Question,
                "content_type": ContentType.objects.get_for_model(Question),
                "objs_list": [],
                "max_size": MAX_RANDOM_QUESTIONS
            },
            "answer": {
                "model": Answer,
                "content_type": ContentType.objects.get_for_model(Answer),
                "objs_list":[],
                "max_size": MAX_RANDOM_ANSWERS
            }
        }
        content_type_tuple = ("question", "answer")

        votes_count = 0
        unique_votes_values = set()
        while votes_count < MAX_RANDOM_VOTES:
            chunk = CHUNK_SIZE if MAX_RANDOM_VOTES - votes_count > CHUNK_SIZE else MAX_RANDOM_VOTES - votes_count
            votes_objs_list = []
            for i in range(votes_count + 1, votes_count + chunk + 1):
                random_content = content_type_tuple[random.randint(0, 1)]
                random_content = vote_setting[random_content]
                random_object_id = random.randint(1, random_content["max_size"])
                random_content_type = random_content["content_type"]

                random_vote = random.randint(0, 1)
                random_vote = 1 if random_vote else -1

                random_user_id = random.randint(1, MAX_RANDOM_USER)

                key = "{}.{}.{}".format(random_user_id, random_content_type, random_object_id)
                if key not in unique_votes_values:
                    unique_votes_values.add(key)

                    vote = Vote(
                        id=i,
                        user_vote=random_vote,
                        user_id=random_user_id,
                        content_type=random_content_type,
                        object_id=random_object_id
                    )
                    votes_objs_list.append(vote)
            Vote.objects.bulk_create(votes_objs_list)
            votes_count += chunk

        self.stdout.write("Generation Votes is success!")
        self.stdout.write("Generation data is success!")