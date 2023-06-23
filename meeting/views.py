from django.http import HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from rest_framework import generics

from meeting.models import Meeting
from meeting.serializers import MeetingSerializer


class MeetingListCreate(generics.ListCreateAPIView):
    # 미팅 생성 api콜
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MeetingSerializer

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
