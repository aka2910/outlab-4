import json
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .fetch_git import *
from .models import *


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
            if commit:
                user.save()
        try:
            p = Profile(username=self.cleaned_data["username"],
                        first_name=self.cleaned_data["first_name"],
                        last_name=self.cleaned_data["last_name"],
                        follower_count=resp['followers'],
                        avatar_url=resp['avatar_url'],
                        )
            p.save()
            for i in repo['repos']:
                r = Repository(user=p, repo_name=i["name"], repo_stars=i["stars"])
                r.save()
        except Exception as err:
            print(f"Error in fetching details from api : {err}")
        return user
