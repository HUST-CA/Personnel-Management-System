from django.conf.urls import url

from . import views

app_name = 'welcome'
urlpatterns = [
    url('^welcome/$', views.WelcomeView.as_view(), name='welcome'),
]
