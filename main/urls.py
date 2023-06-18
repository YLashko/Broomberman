from django.contrib import admin
from django.urls import include, path
from main.views import *

urlpatterns = [
    path("", main, name="main"),
    path("new_game/", new_game, name="new_game"),
    path("game/", game_view, name="game"),
    path("getmonitordata/", get_monitor_data, name="get_monitor_data"),
    path("getplayerdata/", get_player_data, name="get_player_data"),
    path("setmove/", set_player_move, name="set_move"),
    path("getmovecount/", get_move_count, name="get_move_count"),
    path("monitorneedsupdate/", monitor_needs_update, name="monitor_needs_update")
]
