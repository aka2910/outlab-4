from datetime import datetime
import json
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import get_current_timezone
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

from .fetch_git import *
from .forms import *
from .models import Profile1


class SignUpView(SuccessMessageMixin, generic.CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    success_message = f"User was created successfully"


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
    profile.repos = repo
    profile.last_update = datetime.now(tz=get_current_timezone())
    profile.save()
    print(datetime.now())
    return redirect(f'/profile/{user}', {'profile': profile})
