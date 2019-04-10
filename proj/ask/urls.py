from django.urls import path
from django.conf.urls import url

from .views import (
    ask, login, signup, question, index, index_hot, index_search_by_tag, settings
)

app_name = 'ask'

urlpatterns = [
    path("", index, name="index"),
    path("hot/", index_hot, name="index-hot"),
    url(r"tag/(?P<tag_name>[^/]+)/$", index_search_by_tag, name="index-tag"),
    path("ask/", ask, name="ask"),
    path("question/<int:question_id>/", question, name="question"),
    path("login/", login, name="login"),
    path("signup/", signup, name="register"),
    path("settings/", settings, name="user-settings")
]
