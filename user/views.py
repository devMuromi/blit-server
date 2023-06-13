import requests
from rest_framework import generics
from rest_framework.views import APIView
from user.models import User
from user.serializers import BasicUserSerializer, KakaoUserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import permissions, status


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


class KakaoAuthAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_kakao_id(self, kakao_token: str) -> str:
        KAKAO_API_SERVER_URL = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {kakao_token}", "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
        try:
            response = requests.get(KAKAO_API_SERVER_URL, headers=headers)
            if response.status_code == 200:
                return response.json().get("id")
            elif response.status_code == 401:
                return None
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return None

    def post(self, request):
        kakao_token = request.data.get("kakao_token")
        kakao_id = self.get_kakao_id(kakao_token)
        print("kakao_id:", kakao_id)

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
                serializer = KakaoUserSerializer(data={"kakao_id": kakao_id})
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


# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = BasicUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     # "user": serializer.data,
#                     "message": "register successs",
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )

#             res.set_cookie("access", access_token, httponly=True)
#             res.set_cookie("refresh", refresh_token, httponly=True)

#             return res
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = BasicUserSerializer(user)
        return Response(serializer.data)
