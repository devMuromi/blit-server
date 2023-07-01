from django.urls import path
from user import views

urlpatterns = [
    path("basic/", views.AuthAPIView.as_view()),
    path("kakao/", views.KakaoAuthAPIView.as_view()),
    path("user/", views.UserDetail.as_view()),
    # path("register/", views.RegisterAPIView.as_view()),
    # path("auth/refresh/", views.RegisterAPIView.as_view()),
    path("kakao_pay/", views.update_kakao_pay_code),
]
