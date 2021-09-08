from datetime import datetime
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Profile
from .fetch_git import *
from django.utils.timezone import get_current_timezone

# Create your views here.


class SignUpView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def exploreView(request):
    profiles = Profile.objects.all()
    return render(request, 'explore.html', {'profiles': profiles})


def profileView(request, value):
    user = value
    profile = Profile.objects.get(username=user)
    return render(request, 'profile.html', {'profile': profile})


def updateView(request, value):
    user = value
    profile = Profile.objects.get(username=user)
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
