from django.urls import path
from .import views
urlpatterns = [
    path('register/',views.UserRegistration.as_view(),name='register'),
    path('login/',views.UserLogin.as_view(),name='login'),
    path('profile/',views.UserProfile.as_view(),name='profile'),
    path('changepassword/',views.UserChangePassword.as_view(),name='changepassword'),
    path('send-password-reset-link/',views.SendPasswordResetEmail.as_view(),name='send-password-link'),
    path('reset-password/<uid>/<token>/',views.UserPasswordReset.as_view(),name='reset-password')
]
