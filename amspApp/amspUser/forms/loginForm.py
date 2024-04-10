from captcha.fields import CaptchaField
from django import forms
from django.forms import CharField, IntegerField, DateTimeField


class RegisterationHireForm(forms.Form):
    username = CharField(max_length=30, required=True)
    invalidLogins = IntegerField(required=False)
    password = CharField(max_length=30, required=True, widget=forms.PasswordInput)
    captcha = CaptchaField(required=True)



class LoginForm(forms.Form):
    username = CharField(max_length=30, required=True)
    password = CharField(max_length=30, required=True, widget=forms.PasswordInput)
    captcha = CaptchaField(required=True)



