from datetime import datetime
import json
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import get_current_timezone
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .fetch_git import *
from .forms import *
from .models import Profile1


class SignUpView(generic.FormView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = ''
    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        resp = get_github_users_response(username)
        if resp is not None:
            messages.success(self.request, f" {username} was created successfully! Login Now")
            self.success_url = '../accounts/login'
            return HttpResponseRedirect(self.success_url)
        else:
            self.success_url = '../signup'
            messages.success(self.request, f" {username} could not be created due to bad response from github api")
            return HttpResponseRedirect(self.success_url)


def exploreView(request):
    profiles = Profile1.objects.all()
    return render(request, 'explore.html', {'profiles': profiles})


def profileView(request, value):
    user = value
    profile = Profile1.objects.get(username=user)
    return render(request, 'profile.html', {'profile': profile})


def updateView(request, value):
    user = value
    profile = Profile1.objects.get(username=user)
    resp: json = get_github_users_response(user)
    repo = get_github_repos_response(user)
    if repo is not None:
        repo = filter_json(repo)
    profile.follower_count = resp['followers']
    profile.avatar_url = resp['avatar_url']
    profile.repos = repo
    profile.last_update = datetime.now(tz=get_current_timezone())
    profile.save()
    print(datetime.now())
    return redirect(f'/profile/{user}', {'profile': profile})
