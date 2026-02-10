from django.urls import path
from .views import (
    landing_page,
    login_page,
    signup_page,
    signup,
    signin,
)

urlpatterns = [
    # Pages
    path("", landing_page, name="landing"),
    path("login/", login_page, name="login"),
    path("signup/", signup_page, name="signup"),


    # APIs
    path("api/signup/", signup, name="api-signup"),
    path("api/signin/", signin, name="api-signin"),
]
