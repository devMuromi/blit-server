from rest_framework import serializers
from user.models import User


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data["username"], password=validated_data["password"])
        return user


class KakaoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["kakao_id"]

    def create(self, validated_data):
        user = User.objects.create_kakao_user(kakao_id=validated_data["kakao_id"])
        return user
