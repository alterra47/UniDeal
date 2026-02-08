from django.test import TransactionTestCase, Client
from django.urls import reverse
from marketplace.models import UserCredential
import json
import uuid  # Built-in library for unique IDs

class AuthTestCase(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')

    def test_signup_success(self):
        # Generate unique username
        unique_user = f"user_{uuid.uuid4().hex[:8]}"
        data = {
            "username": unique_user,
            "password": "securepassword123"
        }
        
        response = self.client.post(
            self.signup_url,
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(UserCredential.objects.filter(username=unique_user).exists())
        
        response_data = response.json()
        self.assertIn('token', response_data)
        self.assertEqual(response_data['message'], "User registered successfully")

    def test_signup_duplicate_username(self):
        # Create a unique user first
        duplicate_name = f"dup_{uuid.uuid4().hex[:8]}"
        UserCredential.objects.create(username=duplicate_name, password="password123")
        
        data = {
            "username": duplicate_name,
            "password": "differentpassword"
        }
        
        response = self.client.post(
            self.signup_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_signin_success(self):
        # Setup unique user
        user_name = f"signin_{uuid.uuid4().hex[:8]}"
        password = "correctpassword"
        
        # Note: If your model uses password hashing, ensure you use set_password 
        # or create_user helper if available. 
        user = UserCredential.objects.create(username=user_name)
        user.set_password(password)
        user.save()
        
        data = {
            "username": user_name,
            "password": password
        }

        response = self.client.post(
            self.signin_url,
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())