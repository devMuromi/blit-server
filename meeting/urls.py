from django.urls import path
from meeting import views

urlpatterns = [
    path("meeting/", views.MeetingListCreate.as_view()),
    path("meeting/<str:meeting_code>/", views.MeetingRetrieveUpdate.as_view()),
    path("round/", views.RoundCreate.as_view()),
    path("round/<int:pk>/", views.RoundUpdate.as_view()),
]
