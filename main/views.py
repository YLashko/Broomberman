from django.shortcuts import render, redirect
from django.contrib import messages
from main.ServerGlobalData import ServerGlobalData
from main.forms import UserForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from main.models import Profile

sgd = ServerGlobalData()


def main(request):
    global sgd

    login_form = UserForm()
    context = {
        "login_form": login_form,
        "games": sgd.get_main_screen_data(),
        "user_in_game": not sgd.get_user_game_name(request.user.username) is None
    }
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        action = request.POST.get("action")

        if action == "Register":
            try:
                user = User.objects.create(username=username)
                user.set_password(password)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()

                login(request, user)
            except Exception as e:
                print(e)
                messages.error(request, e)

        elif action == "Login":
            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                else:
                    messages.error(request, "Incorrect username or password")
            except Exception as e:
                print(e)
                messages.error(request, e)

        elif action == "Logout":
            logout(request)

        elif action == "Join":
            game_name = request.POST.get("name")
            passphrase = request.POST.get("passphrase")
            try:
                if not request.user.is_authenticated:
                    raise PermissionError("You need to be logged in to join games!")
                sgd.add_player_to_game(game_name, request.user.username, passphrase)
            except Exception as e:
                messages.error(request, e)

        elif action == "Disconnect":
            try:
                sgd.disconnect_player(request.user.username)
            except Exception as e:
                messages.error(request, e)

        return redirect("main")
    return render(request, "main.html", context)


def new_game(request):
    global sgd
    if request.method == "POST":
        game_config = {
            "name": request.POST.get("name"),
            "passphrase": request.POST.get("password")
        }
        try:
            sgd.add_game(game_config, request.user.username)
            profile = Profile.objects.get(user=request.user)
            profile.game = game_config["name"]
            profile.save()
            return redirect("game")
        except Exception as e:
            messages.error(request, e)
    return render(request, "new_game.html", {})


def game_view(request):
    if request.method == "POST":
        if request.POST.get("action") == "Delete game":
            sgd.remove_game(sgd.get_user_game_name(request.user.username), request.user.username)
    try:
        if not request.user.is_authenticated:
            return redirect("main")
        if not sgd.get_user_game_name(request.user.username):
            return redirect("main")
        game = sgd.get_user_game(request.user.username)
        if game.role(request.user.username) == "Monitor":
            context = game.monitor_data()
            return render(request, "game.html", context)
        else:
            context = game.player_data()
            return render(request, "game.html", context)
    except Exception as e:
        messages.error(request, e)
