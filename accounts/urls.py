from django.urls import path,include
from django.conf.urls import url,include
from . import views
from django.contrib.auth.views import (
    LoginView,LogoutView,PasswordResetView,
    PasswordResetDoneView,PasswordResetConfirmView,
    PasswordResetCompleteView,
)


urlpatterns=[
    path('',views.home),
    #path('login',views.login,name='login'),
    path('login/',LoginView.as_view(template_name='accounts/login.html'),{'redirect_if_logged_in': '/'},name='login'),
    path('accounts/login/',LoginView.as_view(template_name='accounts/login.html'),name='logout'),
    path('logout',views.logout),
    path('register',views.register,name='register'),
    url(r'^profile/(?P<pk>\d+)/$', views.profile, name='profile_with_pk'),
    path('profile',views.profile,name='profile'),
    path('profile/edit',views.edit,name='edit'),
    path('password/',views.password,name='password'),
    path('password_reset',PasswordResetView.as_view(template_name='accounts/password_reset.html'),name="password_reset"),
    path('password_reset_done',PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name="password_reset_done"),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete',PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name="password_reset_complete"),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),

]
