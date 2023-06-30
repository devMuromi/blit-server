from django.urls import path
from meeting import views

urlpatterns = [
    path("", views.MeetingListCreate.as_view()),
    path("round", views.RoundCreate.as_view()),
]
