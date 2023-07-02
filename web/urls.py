from django.urls import path
from web import views

urlpatterns = [
    path("", views.meeting),
    path("kakao_callback/", views.kakao_callback),
    path("join_meeting/", views.join_meeting),
    path("join_round/", views.join_round),
    # path("<int:pk>/", views.ReceiptDetail.as_view()),
]
