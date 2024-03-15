import datetime
from uuid import uuid4

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import re

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from AppForTest.models import userData, Session


class LoginPage(APIView):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return HttpResponseRedirect(f"/user/{request.user.username}")
        else:
            return render(request, 'auth/login.html')


class LoginProcceed(APIView):
    def post(self, request) -> HttpResponse:
        if request.data.__contains__('email') and request.data.__contains__('password'):
            results = User.objects.filter(email__exact=request.data.get('email'))
            if len(results) > 0:
                user = User.objects.get(email__exact=request.data.get('email'))
                if user.password.__eq__(request.data.get('password')):
                    token = RefreshToken.for_user(user)
                    userdata = userData.objects.get(user=user)
                    return Response({'status': "ok", "content": {"token": str(token.access_token),
                                                          "user": {'id': user.id, 'username': user.username,
                                                                   'first_name': user.first_name,
                                                                   'last_name': user.last_name, 'photo_url': userdata.UserPicture.url}}})
                else:
                    return Response({'status': "err", "content": {"text": "Неверный логин или пароль"}},)
            else:
                return Response({'status': "err", "content": {"text": "Пользователь не существует"}})
        else:
            return Response({'status': "err", "content": {"text": "Заполнены не все поля"}})
class SignupPage(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return HttpResponseRedirect(f"/user/{request.user.username}")
        else:
            return render(request, 'auth/signup.html')

class UserData:
    def __init__(self, data: list):
        self.raw_data = data

    @property
    def username(self): return self.raw_data[0]

    @property
    def email(self): return self.raw_data[1]

    @property
    def name(self): return self.raw_data[2]

    @property
    def lastname(self): return self.raw_data[3]

    @property
    def password(self): return self.raw_data[4]
    def isEmailValid(self) -> bool:
        print(f"incorrectEmail: {self.email}")
        return re.match(re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"), self.email)

    def isNameValid(self) -> bool:
        print(f"incorrectName: {self.name} {self.lastname}")
        return re.match(re.compile(r"^[a-zA-Zа-яА-Я]+$"), self.name) and re.fullmatch(re.compile("^[a-zA-Zа-яА-Я]+$"), self.lastname)

    def isUsernameValid(self) -> bool:
        print(f"incorrectUsername: {self.username}")
        return re.match(re.compile(r"^[a-zA-Z0-9]+$"), self.username)


    def isValid(self) -> bool:
        return self.isEmailValid() and self.isNameValid() and self.isUsernameValid()
class SignupProcceed(APIView):
    def post(self, request) -> HttpResponse:
        if request.data.__contains__('first_name') and request.data.__contains__('last_name') and request.data.__contains__('email') and request.data.__contains__('password') and request.data.__contains__('username'):
            data = UserData([request.data.get('username'), request.data.get('email'), request.data.get('first_name'), request.data.get('last_name'), request.data.get('password')])
            if data.isValid():
                name_results = User.objects.filter(username=data.username)
                email_results = User.objects.filter(email=data.email)
                if (name_results.count() < 1) and (email_results.count() < 1):
                    user = User(username=data.username,
                                email=data.email,
                                password=data.password,
                                first_name=data.name,
                                last_name=data.lastname
                                )
                    user.save()

                    userdata = userData(user=user)
                    userdata.save()
                    token = RefreshToken.for_user(user)
                    return Response({"status": "ok", "content": {"token": str(token.access_token), "user": {"id": user.id, "username": user.username, "first_name": user.first_name, "last_name": user.last_name, "photo_url": userdata.UserPicture.url}}})
                else:
                    return Response({'status': "err", "content": {
                        "text": "Пользователь с такими данными уже существует"}})
            else:
                return Response({'status': "err", "content": {"text": "Данные некорректны"}})
        else:
            return JsonResponse({'status': "err", "content": {"text": "Заполнены не все поля"}})