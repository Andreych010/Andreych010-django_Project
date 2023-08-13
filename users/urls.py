from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, user_gen_password, ConfirmView, UserLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/genpassword/', user_gen_password, name='genpassword'),
    path('confirm/', ConfirmView.as_view(), name='confirm')
]
