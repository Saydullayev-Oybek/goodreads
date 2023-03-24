import form as form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(
            self.cleaned_data['password']
        )
        user.save()

        return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')