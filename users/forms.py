import form as form
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

from .models import CustomUser
from django import forms


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(
            self.cleaned_data['password']
        )
        user.save()

        # if user.email:
        #     send_mail(
        #         'welcome to goodreads clone',
        #         f"hi, {user.username}, Welcome to goodreads clone",
        #         'oybekjohn01@gmail.com',
        #         [user.email]
        #     )

        return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'image')