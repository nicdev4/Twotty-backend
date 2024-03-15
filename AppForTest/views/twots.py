import datetime

import pytz
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from AppForTest.models import Twot, userData, Session


class Send(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request) -> HttpResponse:
        if request.data.__contains__('text') and len(request.data.get('text')) > 0:
            userdata = userData(user=request.user)
            twot = Twot(user=request.user, userdata=userdata, text=request.data.get('text'),
                        date=datetime.datetime.now())
            twot.save()
            return Response(
                {'status': "ok", 'content': {'twot': {'text': twot.text, 'date': twot.date, 'user': twot.user.id}}})
        else:
            return Response({'status': "err", "content": {"text": "Твот не может быть пустым D:"}})
