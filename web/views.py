from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import requests
from user.views import get_kakao_id
from user.models import User
from django.contrib.auth import login, authenticate
from meeting.models import Meeting, Round
from django.http import JsonResponse
import json
from user.serializers import KakaoUserSerializer


def kakao_login():
    pass


def meeting(request):
    meeting_code = request.GET.get("meeting_code")

    if meeting_code is None or not Meeting.objects.filter(meeting_code=meeting_code).exists():  # 모임 코드가 없거나 오류일 경우
        return HttpResponse("존재하지 않는 모임입니다.")

    meeting = Meeting.objects.get(meeting_code=meeting_code)
    user = request.user

    if not user.is_authenticated:  # 비로그인시 로그인 페이지로 리다이렉트
        client_id = settings.KAKAO_REST_API_KEY
        redirect_uri = f"http://{settings.SERVER_ADDRESS}/meeting/kakao_callback"
        state = meeting_code
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&state={state}&response_type=code",
            target="_blank",
        )

    # 초대가 안된 경우 -> 초대 참여창
    if not user in meeting.attendants.all():
        context = {"meeting_code": meeting_code}
        return render(request, "invite.html", context)

    # 초대가 된 경우
    # 모임 진행중인 경우 -> n차 참여했는지 확인
    if meeting.is_active:
        current_round = Round.objects.filter(meeting=meeting).order_by("-round_number")[0]
        is_attending = current_round.attendants.filter(id=user.id).exists()
        context = {
            "meeting_code": meeting_code,
            "current_round_no": current_round.round_number,
            "is_attending": is_attending,
        }
        return render(request, "meeting.html", context)
    # 모임이 끝나고 송금이 남은 경우 -> 카카오페이 송금 링크
    else:
        total_cost = 0
        for round in meeting.rounds.all():
            if round.attendants.filter(id=user.id).exists():
                total_cost += round.cost / round.attendants.count()
        total_cost = int(total_cost)
        kakao_pay_code = meeting.created_by.kakao_pay_code

        def to_hex_value(value):
            return hex(value * 524288)[2:]

        total_cost_converted = to_hex_value(total_cost)
        context = {
            "total_cost": total_cost,
            "kakaopay_link": f"https://qr.kakaopay.com/{kakao_pay_code}{total_cost_converted}",
        }

        return render(request, "pay.html", context)


def join_meeting(request):
    print("haha")
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        meeting_code = body["meeting_code"]
        print(meeting_code)
        meeting = Meeting.objects.get(meeting_code=meeting_code)
        print(meeting)
        user = request.user
        meeting.attendants.add(user)
        meeting.save()
        response_data = {"message": "모임에 성공적으로 참여했습니다."}
        return JsonResponse(response_data)
    else:
        response_data = {"message": "잘못된 요청입니다."}
        return JsonResponse(response_data, status=400)


def join_round(request):
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        meeting_code = body["meeting_code"]
        meeting = Meeting.objects.get(meeting_code=meeting_code)
        user = request.user
        round = Round.objects.filter(meeting=meeting).order_by("-round_number")[0]
        round.attendants.add(user)
        round.save()
        response_data = {"message": "성공적으로 참여했습니다."}
        return JsonResponse(response_data)
    else:
        response_data = {"message": "잘못된 요청입니다."}
        return JsonResponse(response_data, status=400)


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
        "redirect_uri": f"http://{settings.SERVER_ADDRESS}/meeting/kakao_callback",
        "code": code,
    }
    res = requests.post(TOKEN_URL, data=data).json()
    access_token = res.get("access_token")
    id_token = res.get("id_token")
    expires_in = res.get("expires_in")
    refresh_token = res.get("refresh_token")
    refresh_token_expires_in = res.get("refresh_token_expires_in")

    kakao_id, kakao_name = get_kakao_id(access_token)
    print(kakao_id)
    if kakao_id is not None:  # 무사히 kakao_id를 받아왔을 때
        if User.objects.filter(kakao_id=kakao_id).exists():  # 이미 회원인 경우
            user = User.objects.get(kakao_id=kakao_id)
            print("로그인 id: ", type(user))
            if user is not None:
                login(request, user)
                return redirect(f"/meeting?meeting_code={state}")

        else:  # 회원이 아닌 경우
            serializer = KakaoUserSerializer(data={"kakao_id": kakao_id, "kakao_name": kakao_name})
            if serializer.is_valid():
                user = serializer.save()
                print("회원가입 id: ", type(user))
                user = User.objects.get(kakao_id=kakao_id)
                if user is not None:
                    login(request, user)
                    return redirect(f"/meeting?meeting_code={state}")
            else:
                return HttpResponse("회원가입 실패")

    else:
        # if token is not valid
        return HttpResponse("토큰이 유효하지 않습니다.")

