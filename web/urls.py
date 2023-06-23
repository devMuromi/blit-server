from django.urls import path
from web import views

urlpatterns = [
    path("", views.meeting),
    path("kakao_callback", views.kakao_callback),
    # path("<int:pk>/", views.ReceiptDetail.as_view()),
]
