from django import forms


class RegisterForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField()
    password_repeat = forms.CharField()


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField()
