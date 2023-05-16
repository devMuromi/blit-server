from rest_framework import generics
from user.models import User
from user.serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status


class AuthAPIView(APIView):
    # def get(self, request):
    #     try:
    #         # access token을 decode 해서 유저 id 추출 => 유저 식별
    #         access = request.COOKIES["access"]
    #         payload = jwt.decode(access, SECRET_KEY, algorithms=["HS256"])
    #         pk = payload.get("user_id")
    #         user = get_object_or_404(User, pk=pk)
    #         serializer = UserSerializer(instance=user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     except jwt.exceptions.ExpiredSignatureError:
    #         # 토큰 만료 시 토큰 갱신
    #         data = {"refresh": request.COOKIES.get("refresh", None)}
    #         serializer = TokenRefreshSerializer(data=data)
    #         if serializer.is_valid(raise_exception=True):
    #             access = serializer.data.get("access", None)
    #             refresh = serializer.data.get("refresh", None)
    #             payload = jwt.decode(access, SECRET_KEY, algorithms=["HS256"])
    #             pk = payload.get("user_id")
    #             user = get_object_or_404(User, pk=pk)
    #             serializer = UserSerializer(instance=user)
    #             res = Response(serializer.data, status=status.HTTP_200_OK)
    #             res.set_cookie("access", access)
    #             res.set_cookie("refresh", refresh)
    #             return res
    #         raise jwt.exceptions.InvalidTokenError

    #     except jwt.exceptions.InvalidTokenError:
    #         # 사용 불가능한 토큰일 때
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def post(self, request):
        # 유저 인증
        user = authenticate(kakao_id=request.data.get("kakao_id"))
        # 카카오 토큰을 받아서 유저 인증하는 파트가 여기 들어가야함.
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    # "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            # res.set_cookie("access", access_token, httponly=True)
            # res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({"message": "Logout success"}, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    # "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    # lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# class MyPage(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user


######## kakao
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        kakao_id = request.data.get("kakao_id")
        email = request.data.get("email")
        # 기타 필요한 사용자 정보

        try:
            user = User.objects.get(kakao_id=kakao_id)
            return Response({"detail": "User already exists."}, status=400)
        except User.DoesNotExist:
            user = User.objects.create(kakao_id=kakao_id, email=email)
            return Response({"detail": "User successfully created."}, status=201)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        kakao_id = request.data.get("kakao_id")

        try:
            user = User.objects.get(kakao_id=kakao_id)
            # 로그인 처리를 위한 적절한 로직을 수행합니다.
            # 예시: 토큰 기반 인증을 사용하여 사용자를 로그인 상태로 유지합니다.
            return Response({"detail": "User logged in successfully."}, status=200)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=404)
