from django.urls import path
from meeting import views

urlpatterns = [
    path("", views.MeetingListCreate.as_view()),
    # path("<int:pk>/", views.ReceiptDetail.as_view()),
]