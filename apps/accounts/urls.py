from apps.accounts import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("change_password/", views.change_password, name="change_password"),

    #todo : reset password with email
]
