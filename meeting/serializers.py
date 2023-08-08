from rest_framework import serializers
from datetime import datetime
from django.utils.crypto import get_random_string

from meeting.models import Meeting, Round


class MeetingSerializer(serializers.ModelSerializer):
    attendants = serializers.SerializerMethodField()
    meeting_code = serializers.CharField(required=False)
    rounds = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = ("name", "created_by", "created_at", "meeting_code", "attendants", "is_active", "rounds")

    def create(self, validated_data):
        meeting = super().create(validated_data)
        name = validated_data.get("name")
        meeting.created_by = self.context["request"].user
        meeting.is_active = True

        # 무작위 문자열 중복 없을때까지 생성
        meeting_code = get_random_string(length=10)
        while Meeting.objects.filter(meeting_code=meeting_code).exists():
            meeting_code = get_random_string(length=10)
        meeting.meeting_code = meeting_code

        meeting.save()
        return meeting

    def get_attendants(self, obj):
        return obj.attendants.values_list("kakao_name", flat=True)

    def get_rounds(self, obj):
        rounds = obj.rounds.values("round_number", "cost")
        result = []
        for round in rounds:
            round_data = {
                "round_number": round["round_number"],
                "attendants": list(
                    obj.rounds.filter(round_number=round["round_number"]).values_list("attendants__kakao_name", flat=True)
                ),
                "cost": round["cost"],
            }
            result.append(round_data)
        return result


class RoundSerializer(serializers.ModelSerializer):
    # meeting_code = serializers.CharField(write_only=True)
    round_number = serializers.IntegerField(read_only=True)
    cost = serializers.IntegerField(required=False)

    class Meta:
        model = Round
        exclude = ["meeting"]

    def create(self, validated_data):
        meeting_code = self.context["request"].query_params.get("meeting_code")
        try:
            meeting = Meeting.objects.get(meeting_code=meeting_code)  # meeting_code를 사용하여 해당 meeting 객체 가져오기
        except Meeting.DoesNotExist:
            raise serializers.ValidationError("Invalid meeting code.")  # 유효하지 않은 meeting_code인 경우 예외 처리

        owner = self.context["request"].user  # 현재 사용자의 meeting 가져오기
        validated_data["attendants"] = [owner.pk]  # meeting의 소유자를 attendants에 포함
        validated_data["cost"] = 0  # cost 필드 자동으로 0으로 설정
        validated_data["round_number"] = meeting.rounds.count() + 1
        validated_data["meeting"] = meeting

        round = super().create(validated_data)
        round.meeting = meeting
        round.save()
        return round

    def update(self, instance, validated_data):
        meeting_code = self.context["request"].query_params.get("meeting_code")
        try:
            meeting = Meeting.objects.get(meeting_code=meeting_code)  # meeting_code를 사용하여 해당 meeting 객체 가져오기
        except Meeting.DoesNotExist:
            raise serializers.ValidationError("Invalid meeting code.")  # 유효하지 않은 meeting_code인 경우 예외 처리

        round_number = self.context["view"].kwargs.get("pk")
        print(round_number)
        cost = validated_data.get("cost")

        try:
            round = meeting.rounds.get(round_number=round_number)
        except Round.DoesNotExist:
            raise serializers.ValidationError("Invalid round number.")

        if cost is not None:
            round.cost = cost
        round.save()

        return round
