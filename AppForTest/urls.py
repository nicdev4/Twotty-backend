"""
URL configuration for AppForTest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from AppForTest.views import sign, profile, twots, home, sessions

urlpatterns = [
    path('index/', home.HomePage.as_view()),
    path('admin/', admin.site.urls),
    path('login/', csrf_exempt(sign.LoginProcceed.as_view())),
    path('signup/', csrf_exempt(sign.SignupProcceed.as_view())),
    path('logout/', profile.Logout.as_view()),
    path('user/<str:username>/', profile.UserProfilePage.as_view()),
    path('user/<str:username>/twots', profile.UserTwots.as_view()),
    path('send/', csrf_exempt(twots.Send.as_view())),
    path('session/', sessions.SessionCheck.as_view()),
    path('session/<str:token>', sessions.SessionCheck.as_view()),
    path('api/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
