from django.db import models
from user.models import User


# 각 회식
class Meeting(models.Model):
    name = models.TextField()
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)
    meeting_code = models.TextField(unique=True)  # URL에 들어갈 랜덤 문자열
    attendants = models.ManyToManyField(User, related_name="meetings", null=True)
    is_active = models.BooleanField(default=True)  # 회식이 진행중인지 여부
    # round_set

    def __str__(self):
        return f"{self.name} By {self.created_by.username}"


# 1차, 2차, 3차 라운드
class Round(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="rounds")
    round_number = models.IntegerField()
    cost = models.IntegerField()
    attendants = models.ManyToManyField(User, related_name="rounds", through="Attend")

    def __str__(self):
        return f"{self.meeting.name} Round {self.round_number}"

    class Meta:
        # 각 회식당 같은 차수의 라운드가 유일하게 제한
        constraints = [
            models.UniqueConstraint(fields=["meeting", "round_number"], name="unique round in meeting"),
        ]


# 각 라운드별 참여인원, Round-User m2m 중간 모델
class Attend(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    attendant = models.ForeignKey(User, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)  # 참여 여부
