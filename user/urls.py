from django.urls import path
from user import views


urlpatterns = [
    path("register/", views.RegisterAPIView.as_view()),
    path("auth/", views.AuthAPIView.as_view()),
    # path("auth/refresh/", views.RegisterAPIView.as_view()),
]
