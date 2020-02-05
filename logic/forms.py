from django import forms
from datamodel.models import Game, Move, Counter
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignupForm(forms.ModelForm):
    password = forms.CharField(min_length=1, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=1, required=True, widget=forms.PasswordInput)

    def clean_password(self):
        p1 = self.cleaned_data.get("password")
        if len(p1) < 5:
            raise ValidationError(
                "password too common or password is too short "
                "make sure it has at least 6 characters")
        else:
            return p1

    def clean_password2(self):
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("password2")

        if p1 != p2:
            raise ValidationError(
                "Password and Repeat password are not the same|"
                "La clave y su repetición no coinciden")
        else:
            return p2

    class Meta:
        model = User
        fields = ('username', 'password', "password2")


class MoveForm(forms.ModelForm):
    origin = forms.IntegerField(min_value=0, max_value=63, required=False, widget=forms.HiddenInput())
    target = forms.IntegerField(min_value=0, max_value=63, required=False, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('origin', 'target')
