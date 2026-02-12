
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from .models import UserCredential
from .serializer import SignupSerializer, SigninSerializer
from django.shortcuts import render



# ======================
# PAGE VIEWS (HTML)
# ======================

def landing_page(request):
    return render(request, "main-before-login.html")

def signin_page(request):
    return render(request, "login-main.html")

def signup_page(request):
    return render(request, "signup-main.html")


def get_token_for_user(user):
    """Generate single JWT access token"""
    token = AccessToken()
    token['username'] = user.username
    return str(token)

@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        token = get_token_for_user(user)
        return Response(
            {
                "message": "User registered successfully",
                "token": token
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signin(request):
    serializer = SigninSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    try:
        user = UserCredential.objects.get(username=username)
    except UserCredential.DoesNotExist:
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.verify_password(password):
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token = get_token_for_user(user)

    return Response(
        {
            "message": "Login successful",
            "token": token
        },
        status=status.HTTP_200_OK
    )