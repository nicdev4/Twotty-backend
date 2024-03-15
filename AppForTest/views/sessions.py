import datetime

import pytz
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

from AppForTest.models import userData, Twot, Session


class SessionCheck(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs) -> HttpResponse:
        user = request.user
        userdata = userData.objects.get(user=user)
        return Response({'status': 'ok',
                         'content': {'id': user.id, 'username': user.username, 'first_name': user.first_name,
                                     'last_name': user.last_name, 'photo_url': userdata.UserPicture.url}})
