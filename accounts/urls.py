
from django.urls import path
from knox import views as knox_views

from .api import RegisterAPI, LoginAPI, UserAPI, UserRegisterAPI


urlpatterns = [
    # path('', include('knox.urls')),
    path('register', RegisterAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('user', UserAPI.as_view()),
    path('profile', UserRegisterAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout')

]
