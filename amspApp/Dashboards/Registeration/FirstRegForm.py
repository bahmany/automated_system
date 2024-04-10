# coding=utf-8
from captcha.fields import CaptchaField
from django.forms import forms, CharField, PasswordInput


class FirstRegForm(forms.Form):
    captcha = CaptchaField(required=True)
    cellNo = CharField(min_length=11, max_length=11, required=True)
    password = CharField(min_length=3, max_length=50, required=True, widget=PasswordInput())


class ForgetPassForm(forms.Form):
    captcha = CaptchaField(required=True)
    cellNo = CharField(min_length=3, max_length=19, required=True)
