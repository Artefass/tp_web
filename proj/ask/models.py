from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Sum


# model manager

class QuestionModelManager(models.Manager):

    def hot(self):
        return self.get_queryset().order_by("-raiting")

    def new(self):
        return self.get_queryset().order_by("-creation_date")


class VoteManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_raiting(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('user_vote')).get('user_vote__sum') or 0

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    tags = models.ManyToManyField('Tag')
    raiting = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now=True)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = GenericRelation('Vote', related_query_name='questions')

    objects = QuestionModelManager()

class Tag(models.Model):
    name = models.CharField(max_length=16)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raiting = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now=True)
    correct = models.BooleanField(default=False)
    votes   = GenericRelation('Vote', related_query_name='answers')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=16)
    avatar   = models.FileField()
    raiting  = models.IntegerField(default=0)

class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_vote = models.SmallIntegerField(choices=VOTES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id    = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = VoteManager()




