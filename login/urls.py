from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
]
