from rest_framework import serializers
from user.models import User


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ("username", "is_staff", "kakao_id", "kakao_pay_code")

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data["username"], password=validated_data["password"])
        return user


class KakaoUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)  # 선택적 필드로 설정

    class Meta:
        model = User
        fields = ("username", "is_staff", "kakao_id", "kakao_name")

    def create(self, validated_data):
        user = User.objects.create_kakao_user(kakao_id=validated_data["kakao_id"], kakao_name=validated_data["kakao_name"])
        return user
