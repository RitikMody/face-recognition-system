from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('activate/<slug:uidb64>/<slug:token>/',
         views.activate, name='activate')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
