from rest_framework.permissions import BasePermission

from meeting.models import Meeting


class IsRoundOwner(BasePermission):
    def has_permission(self, request, view):
        meeting_code = request.GET.get("meeting_code")
        if meeting_code is None:
            return False
        meeting = Meeting.objects.get(meeting_code=meeting_code)

        # 요청한 사용자와 meeting 소유자를 비교하여 권한 확인
        return request.user == meeting.created_by


class IsMeetingOwner(BasePermission):
    def has_permission(self, request, view):
        meeting_code = view.kwargs.get("meeting_code")
        if meeting_code is None:
            return False
        meeting = Meeting.objects.get(meeting_code=meeting_code)
        return request.user == meeting.created_by
