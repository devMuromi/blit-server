from django.http import HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions

from meeting.permissions import IsMeetingOwner


from meeting.models import Meeting, Round
from meeting.serializers import MeetingSerializer, RoundSerializer


class MeetingListCreate(generics.ListCreateAPIView):
    # 미팅 생성 api콜
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MeetingSerializer

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RoundCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsMeetingOwner]
    serializer_class = RoundSerializer

    def perform_create(self, serializer):
        serializer.save()
