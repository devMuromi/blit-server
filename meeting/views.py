from django.http import HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from rest_framework import generics

from meeting.models import Meeting
from meeting.serializers import MeetingSerializer

# 회식을 만드는 뷰
# 초대 url로 접속가능한 템플릿
# 회식관리 뷰로서 1차 끝나는등 했을때 전송하는 뷰 되면 자동으로 문자도 보내야함
# 회식 끝나면 접속가능한 링크. 페이먼트 만드는 뷰


def meeting(request):
    # 초대가 안된경우 -> 초대 참여창

    # 초대가 되어 이미 회원인경우 -> 각 라운드별 화면 표시
    pass
    # 라운드가 끝나고 pay가 남은경우 -> 금액과 송금 표시


class MeetingListCreate(generics.ListCreateAPIView):
    # 미팅 생성 api콜
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MeetingSerializer

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
