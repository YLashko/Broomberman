from django.contrib import admin
from django.urls import include, path
from main.views import *

urlpatterns = [
    path("", main, name="main"),
    path("new_game/", new_game, name="new_game"),
    path("game/", game_view, name="game")
]
