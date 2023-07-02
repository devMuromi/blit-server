from django.db import models
from user.models import User


# 각 회식
class Meeting(models.Model):
    name = models.TextField()
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)
    meeting_code = models.TextField(unique=True)  # URL에 들어갈 랜덤 문자열
    attendants = models.ManyToManyField(User, related_name="meetings", blank=True)
    is_active = models.BooleanField(default=True)  # 회식이 진행중인지 여부
    # rounds

    def __str__(self):
        return f"{self.name} By {self.created_by.username}"

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the Meeting is being created or updated
        super().save(*args, **kwargs)
        if created:
            round = Round.objects.create(meeting=self, round_number=1, cost=0)  # Create Round 1
            round.attendants.add(self.created_by)  # Add the creator to Round 1
            self.attendants.add(self.created_by)  # Add the creator to attendants


# 1차, 2차, 3차 라운드
class Round(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="rounds")
    round_number = models.IntegerField()
    cost = models.IntegerField()
    attendants = models.ManyToManyField(User, related_name="rounds", blank=True)

    def __str__(self):
        return f"{self.meeting.name} Round {self.round_number}"

    class Meta:
        # 각 회식당 같은 차수의 라운드가 유일하게 제한
        constraints = [
            models.UniqueConstraint(fields=["meeting", "round_number"], name="unique round in meeting"),
        ]
