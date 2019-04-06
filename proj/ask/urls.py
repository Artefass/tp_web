from django.urls import path
from django.conf.urls import url

from .views import (
    ask, login, signup, question, index, settings
)

app_name = 'ask'

urlpatterns = [
    path("", index, name="index"),
    url(r"tag/(?P<tag>[^/]+)/$", index, name="index-tag"),
    path("ask/", ask, name="ask"),
    path("question/<int:question_id>/", question, name="question"),

    #path("tag/<tag_name>/", index, 'index'),

    path("login/", login, name="login"),
    path("register/", signup, name="register"),
    path("settings/", settings, name="user-settings")
]
