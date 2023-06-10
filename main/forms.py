from django.forms import ModelForm, Form, CharField, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(Form):
    username = CharField(max_length=20)
    password = CharField(widget=PasswordInput())
