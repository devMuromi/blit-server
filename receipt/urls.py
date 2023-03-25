from django.urls import path
from receipt import views

urlpatterns = [
    path("", views.ReceiptList.as_view()),
    path("<int:pk>/", views.ReceiptDetail.as_view()),
]
