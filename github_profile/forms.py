import json

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .fetch_git import *
from .models import Profile


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name")

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        resp: json = get_github_users_response(self.cleaned_data["username"])
        repo = get_github_repos_response(self.cleaned_data["username"])
        if repo is not None:
            repo = filter_json(repo)
        # print(resp)
        try:
            Profile.objects.create(username=self.cleaned_data["username"],
                                   first_name=self.cleaned_data["first_name"],
                                   last_name=self.cleaned_data["last_name"],
                                   follower_count=resp['followers'],
                                   repos=repo
                                   )
        except Exception as err:
            print(f"Error in fetching details from api : {err}")
        if commit:
            user.save()
        return user
