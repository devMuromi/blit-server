import requests
from rest_framework.views import APIView
from user.models import User
from user.serializers import BasicUserSerializer, KakaoUserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


class AuthAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if user is not None:
            serializer = BasicUserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "message": "login success",
                    "user": serializer.data,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response(
                {
                    "message": "invalid account",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


def get_kakao_id(kakao_token: str):
    KAKAO_API_SERVER_URL = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {kakao_token}", "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    try:
        response = requests.get(KAKAO_API_SERVER_URL, headers=headers)
        if response.status_code == 200:
            kakao_id = response.json().get("id")
            kakao_name = response.json().get("properties").get("nickname")
            return (kakao_id, kakao_name)
        elif response.status_code == 401:
            return None
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None


class KakaoAuthAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        kakao_token = request.data.get("kakao_token")
        kakao_id, kakao_name = get_kakao_id(kakao_token)

        if kakao_id is not None:
            if User.objects.filter(kakao_id=kakao_id).exists():
                user = User.objects.get(kakao_id=kakao_id)
                serializer = KakaoUserSerializer(user)
                token = TokenObtainPairSerializer.get_token(user)
                refresh_token = str(token)
                access_token = str(token.access_token)
                res = Response(
                    {
                        "message": "login success",
                        "user": serializer.data,
                        "token": {
                            "access": access_token,
                            "refresh": refresh_token,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            else:
                serializer = KakaoUserSerializer(data={"kakao_id": kakao_id, "kakao_name": kakao_name})
                if serializer.is_valid():
                    user = serializer.save()
                    token = TokenObtainPairSerializer.get_token(user)
                    refresh_token = str(token)
                    access_token = str(token.access_token)
                    res = Response(
                        {
                            "message": "register success",
                            "user": serializer.data,
                            "token": {
                                "access": access_token,
                                "refresh": refresh_token,
                            },
                        },
                        status=status.HTTP_200_OK,
                    )
                    return res
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            # if token is not valid
            return Response(
                {
                    "message": "invalid token",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = BasicUserSerializer(user)
        return Response(serializer.data)


@api_view(["POST"])
@login_required
def update_kakao_pay_code(request):
    user = request.user
    kakao_pay_code = request.data.get("kakao_pay_code")

    if not kakao_pay_code:
        return Response({"error": "kakao_pay_code field is required."}, status=400)

    user.kakao_pay_code = kakao_pay_code
    user.save()

    return JsonResponse({"success": "kakao_pay_code has been updated."})
