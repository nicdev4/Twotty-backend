from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import re

from AppForTest.models import userData, Twot

class HomePage(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        data = Twot.objects.all().order_by('-id')[:12]
        twots = []
        for twot in data:
            user = twot.user
            userdata = twot.userdata
            twots.append({'twot': {'text': twot.text, 'creation_date': twot.date}, 'author': {'username': user.username, 'photo': userdata.UserPicture.url}})
        resp = JsonResponse({'status': 'ok', 'content': twots})
        return resp