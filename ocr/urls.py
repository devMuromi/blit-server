from django.urls import path
from ocr import views

urlpatterns = [
    path("<int:pk>/", views.ocr),
]
