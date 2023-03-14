from django.urls import path
from image import views

urlpatterns = [
    path('image/', views.image_list),
    path('image/<int:pk>/', views.image_detail),
]