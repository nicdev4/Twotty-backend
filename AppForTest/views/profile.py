from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import re

from AppForTest.models import userData, Twot


class UserProfilePage(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        query_username = kwargs['username']
        query_user = User.objects.filter(username=query_username)
        if query_user.exists():
            del query_user
            user = User.objects.get(username=query_username)
            query_userdata = userData.objects.get(user=user)
            return JsonResponse({'id': user.id, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'photo_url': query_userdata.UserPicture.url})
        else:
            return JsonResponse({'status': 'error', 'content': {'message': 'Кажется, такой страницы не существует.'}})

class UserTwots(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        query_username = kwargs['username']
        query_user = User.objects.filter(username=query_username)
        if query_user.exists():
            del query_user
            user = User.objects.get(username=query_username)
            query_userdata = userData.objects.get(user=user)
            twots_raw = Twot.objects.filter(user=user).order_by('-id')[:15]
            twots = []
            for twot in twots_raw:
                twots.append({'id': twot.id, 'text': twot.text, 'author': twot.user.id, 'date': twot.date})
            return JsonResponse({'content': twots})
        else:
            return JsonResponse({'status': 'err', 'content': {'message': 'Кажется, такой страницы не существует.'}})


class Logout(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect('/login')


