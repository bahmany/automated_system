from django import forms
from captcha.fields import CaptchaField
from django.forms import CharField, EmailField
from amspApp.Infrustructures.Classes.IsEnglish import  isEnglishPassword, isEnglishUsername


class RegisterationLoginForm(forms.Form):
    username = CharField(max_length=30, required=True)
    password = CharField(max_length=30, required=True, widget=forms.PasswordInput)
    captcha = CaptchaField(required=True)


class ForgetForm(forms.Form):
    name = CharField(max_length=80, required=True)
    captcha = CaptchaField(required=True)

class ResetForm(forms.Form):
    password = CharField(max_length=80, min_length=4, required=True, widget=forms.PasswordInput)
    confirmPassword = CharField(max_length=80,min_length=4, required=True, widget=forms.PasswordInput)
    uid = CharField(max_length=98,min_length=95, required=True)
    captcha = CaptchaField(required=True)

    def clean(self):
        password = self.cleaned_data.get('password')
        confirmPassword = self.cleaned_data.get('confirmPassword')
        if password != confirmPassword:
            self.add_error('password', 'رمز عبور از حروف غیر معتبر استفاده شده است')

        return self.cleaned_data


    # def __init__(self, *args, **kwargs):
    #     super(ForgetForm, self).__init__(*args, **kwargs)
    #     self.fields['captcha'].widget.attrs.update({
    #         'autocomplete': 'off',
    #         'ng-model': 'forget.captcha',
    #     })

class RegisterationHireForm(forms.Form):
    name = CharField(min_length=3, max_length=20, required=True)
    family = CharField(min_length=3, max_length=20, required=True)
    username = CharField(min_length=4, max_length=30, required=True)
    password = CharField(min_length=5, max_length=30, required=True, widget=forms.PasswordInput)
    passwordConfirm = CharField(min_length=5, max_length=30, required=True, widget=forms.PasswordInput)
    email = EmailField(min_length=6, max_length=30, required=True)
    captcha2 = CaptchaField(required=True, label="اعتبارسنجی", error_messages={
        'required':'لطفا عکس روبوت را به درستی وارد نمایید',
        'invalid':'لطفا عکس روبوت را به درستی وارد نمایید'
    })

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        passwordConfirm = self.cleaned_data.get('passwordConfirm')
        email = self.cleaned_data.get('email')

        if not isEnglishPassword(password):
            self.add_error('password', 'رمز عبور از حروف غیر معتبر استفاده شده است')
            self.add_error('passwordConfirm', 'رمز عبور از حروف غیر معتبر استفاده شده است')


        if not isEnglishUsername(username):
            self.add_error('username', 'نام کاربری از حروف غیر معتبر استفاده شده است')


        if password and password != passwordConfirm:
            self.add_error('password', 'در ورود تاییدیه ی رمز عبور دقت نمایید')


        return self.cleaned_data


