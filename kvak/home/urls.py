from django.urls import path

from .views import AnswerView

urlpatterns = [
    path("answer/", AnswerView.as_view(), name="answer"),
]
