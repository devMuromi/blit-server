from django.urls import path
from receipt import views

urlpatterns = [
    path("", views.ReceiptListCreate.as_view()),
    path("<int:pk>/", views.ReceiptDetail.as_view()),
]
