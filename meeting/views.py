from django.http import HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

# 회식을 만드는 뷰
# 초대 url로 접속가능한 템플릿
# 회식관리 뷰로서 1차 끝나는등 했을때 전송하는 뷰 되면 자동으로 문자도 보내야함
# 회식 끝나면 접속가능한 링크. 페이먼트 만드는 뷰
