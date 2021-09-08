from django.urls import path

from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('explore/', exploreView, name="explore"),
    path('profile/<str:value>/', profileView, name="profile"),
    path('update/<str:value>/', updateView, name="update"),
]
