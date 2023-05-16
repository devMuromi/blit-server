from django.urls import path
from user import views

urlpatterns = [
    path("kakao/", views.KakaoAuthAPIView.as_view()),
    path("basic/", views.AuthAPIView.as_view()),
    # path("register/", views.RegisterAPIView.as_view()),
    # path("auth/refresh/", views.RegisterAPIView.as_view()),
]
