"""ratonGato_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", views.index, name="landing"),
    path("", views.index, name="index"),
    path("login/", views.login_service, name="login"),
    path("logout/", views.logout_service, name="logout"),
    path("signup/", views.signup_service, name="signup"),
    path("counter/", views.counter, name="counter"),
    path("create_game/", views.create_game_service, name="create_game"),
    path("join_game/", views.join_game, name="join_game"),
    path("select_game/", views.select_game, name="select_game"),
    path("select_game/<int:game_id>/", views.select_game, name="select_game"),
    path("show_game/", views.show_game, name="show_game"),
    path("IA/", views.jugar_vs_ia, name="vsIA"),
    path("move/", views.move_service, name="move"),
    path("repeticion/", views.repeticion_partida, name="repeticion"),
    path("final/", views.partida_terminada, name="fin_partida")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
