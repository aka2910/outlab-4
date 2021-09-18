from datetime import datetime
from django.shortcuts import render, redirect
from django.utils.timezone import get_current_timezone
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .fetch_git import get_github_users_response
from .forms import *
from .models import *


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
    profiles = Profile.objects.all()
    return render(request, 'explore.html', {'profiles': profiles})


def profileView(request, value):
    user = value
    profile = Profile.objects.get(username=user)
    repos = Repository.objects.filter(user__username=user).order_by('-repo_stars')
    print(repos)
    return render(request, 'profile.html', {'profile': profile, 'repos': repos})


def updateView(request, value):
    user = value
    profile = Profile.objects.get(username=user)
    resp: json = get_github_users_response(user)
    repo = get_github_repos_response(user)
    if repo is not None:
        repo = filter_json(repo)
    profile.follower_count = resp['followers']
    profile.avatar_url = resp['avatar_url']
    profile.last_update = datetime.now(tz=get_current_timezone())
    profile.save()
    print(Repository.objects.filter(user__username=user).count())
    Repository.objects.filter(user__username=user).delete()
    print(Repository.objects.filter(user__username=user).count())
    for i in repo['repos']:
        r = Repository(user=profile, repo_name=i["name"], repo_stars=i["stars"])
        r.save()
    print(Repository.objects.filter(user__username=user).count())
    print(datetime.now())
    return redirect(f'/profile/{user}', {'profile': profile})
