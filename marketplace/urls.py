from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.landing_page, name='landing'),
    path('signin/', views.signin_page, name='signin_page'),
    path('signup/', views.signup_page, name='signup_page'),

    # APIs
    path('api/signin/', views.signin, name='signin_api'),
    path('api/signup/', views.signup, name='signup_api'),
]
