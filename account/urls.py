from django.conf.urls import url

from . import views

app_name = 'account'
urlpatterns = [
    url('^register/$', views.RegisterView.as_view(), name='register'),
    url('^login/$', views.LoginView.as_view(), name='login'),
    url('^logout/$', views.LogoutView.as_view(), name='logout'),
    url('^password_change/$', views.PasswordChangeView.as_view(), name='password_change'),
    url('^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    url('^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    url(r'^own/(?P<email_slug>.*?)/$', views.Own.as_view(), name='own'),
]
