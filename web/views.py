from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import requests
from user.views import get_kakao_id
from user.models import User
from django.contrib.auth import login, authenticate
from meeting.models import Meeting


# 회식을 만드는 뷰
# 초대 url로 접속가능한 템플릿
# 회식관리 뷰로서 1차 끝나는등 했을때 전송하는 뷰 되면 자동으로 문자도 보내야함
# 회식 끝나면 접속가능한 링크. 페이먼트 만드는 뷰


def kakao_login():
    pass


def meeting(request):
    meeting_code = request.GET.get("meeting_code")

    if meeting_code is None or not Meeting.objects.filter(meeting_code=meeting_code).exists():  # 모임 코드가 없거나 오류일 경우
        return HttpResponse("존재하지 않는 모임입니다.")

    user = request.user
    if not user.is_authenticated:  # 비로그인시 로그인 페이지로 리다이렉트
        client_id = settings.KAKAO_REST_API_KEY
        redirect_uri = f"http://{settings.SERVER_ADDRESS}/meeting/kakao_callback"
        state = meeting_code
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&state={state}&response_type=code",
            target="_blank",
        )

    print(user)
    return render(request, "invite.html")

    # 초대가 안된경우 -> 초대 참여창

    # 초대가 되어 이미 회원인경우 -> 각 라운드별 화면 표시
    # 라운드가 끝나고 pay가 남은경우 -> 금액과 송금 표시

    # return render(request, "login.html")


def kakao_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    # 인증 실패시
    if code is None:
        error = request.GET.get("error")
        error_description = request.GET.get("error_description")
        return HttpResponse(f"{error}: {error_description}")

    TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",  # authorization_code로 고정
        "client_id": settings.KAKAO_REST_API_KEY,
        "redirect_uri": "http://localhost:8000/meeting/kakao_callback",
        "code": code,
    }
    res = requests.post(TOKEN_URL, data=data).json()
    access_token = res.get("access_token")
    id_token = res.get("id_token")
    expires_in = res.get("expires_in")
    refresh_token = res.get("refresh_token")
    refresh_token_expires_in = res.get("refresh_token_expires_in")

    kakao_id = get_kakao_id(access_token)
    print(kakao_id)
    if kakao_id is not None:  # 무사히 kakao_id를 받아왔을 때
        if User.objects.filter(kakao_id=kakao_id).exists():  # 이미 회원인 경우
            user = User.objects.get(kakao_id=kakao_id)
            print("로그인 id: ", type(user))
            if user is not None:
                login(request, user)
                return redirect(f"/meeting?meeting_code={state}")

        else:  # 회원이 아닌 경우
            serializer = KakaoUserSerializer(data={"kakao_id": kakao_id})
            if serializer.is_valid():
                user = serializer.save()
                print("회원가입 id: ", type(user))
                user = User.objects.get(kakao_id=kakao_id)
                if user is not None:
                    login(request, user)
                    return redirect(f"localhost:8000/meeting?meeting_code={state}")
            else:
                return HttpResponse("회원가입 실패")

    else:
        # if token is not valid
        return HttpResponse("토큰이 유효하지 않습니다.")
