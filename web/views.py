from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import requests

# 회식을 만드는 뷰
# 초대 url로 접속가능한 템플릿
# 회식관리 뷰로서 1차 끝나는등 했을때 전송하는 뷰 되면 자동으로 문자도 보내야함
# 회식 끝나면 접속가능한 링크. 페이먼트 만드는 뷰


def kakao_login():
    pass


def meeting(request):
    user = request.user
    # 로그인이 안된 경우 -> 카카오 로그인

    # 초대가 안된경우 -> 초대 참여창

    # 초대가 되어 이미 회원인경우 -> 각 라운드별 화면 표시
    # 라운드가 끝나고 pay가 남은경우 -> 금액과 송금 표시

    # return render(request, "login.html")
    client_id = settings.KAKAO_REST_API_KEY
    redirect_uri = "http://localhost:8000/meeting/kakao_callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


def kakao_callback(request):
    code = request.GET.get("code")
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
    print(res)
