from rest_framework import serializers
from meeting.models import Meeting
from datetime import datetime
from django.utils.crypto import get_random_string


class MeetingSerializer(serializers.ModelSerializer):
    attendants = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = ("name", "created_by", "created_at", "meeting_code", "attendants", "is_active")

    def create(self, validated_data):
        meeting = super().create(validated_data)
        name = validated_data.get("name")
        meeting.created_by = self.context["request"].user

        # 무작위 문자열 중복 없을때까지 생성
        meeting_code = get_random_string(length=10)
        while Meeting.objects.filter(meeting_code=meeting_code).exists():
            meeting_code = get_random_string(length=10)
        meeting.meeting_code = meeting_code

        meeting.save()
        return meeting

    def get_attendants(self, obj):
        return obj.attendants.values_list("kakao_name", flat=True)
