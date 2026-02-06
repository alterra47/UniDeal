from django.db import models
from core.auth import Password_Hasher 
import bcrypt
# Create your models here.
class UserCredential(models.Model):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password = Password_Hasher(raw_password).decode('utf-8')
    
    def verify_password(self, raw_password):
        """Verify the password against the hash"""
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password.encode('utf-8')
        )
    
    def __str__(self):
        return self.username