# coding=utf-8
from captcha.fields import CaptchaField
from django.forms import forms, CharField, PasswordInput


class LoginForm(forms.Form):
    captcha = CaptchaField(required=True)
    # cellNo = CharField(min_length=13, max_length=13, required=True)
    # password = CharField(min_length=3, max_length=50, required=True, widget=PasswordInput())


