from django.db import models
from core.auth import Password_Hasher
import bcrypt


class UserCredential(models.Model):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
        return f"{self.username} ({self.role})"


class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = Password_Hasher(raw_password).decode('utf-8')

    def verify_password(self, raw_password):
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password.encode('utf-8')
        )

    def __str__(self):
        return self.username


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('books', 'Books'),
        ('furniture', 'Furniture'),
        ('clothing', 'Clothing'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('sold', 'Sold'),
        ('removed', 'Removed by Admin'),
    ]

    seller = models.ForeignKey(
        UserCredential, on_delete=models.CASCADE, related_name='products'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_remarks = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — ₹{self.price} ({self.get_status_display()})"

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='products/%Y/%m/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.title}"


class Interest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='interests'
    )
    buyer = models.ForeignKey(
        UserCredential, on_delete=models.CASCADE, related_name='interests'
    )
    message = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'buyer')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.buyer.username} → {self.product.title} ({self.status})"


class Comment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='comments'
    )
    user = models.ForeignKey(
        UserCredential, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.title}"


class Report(models.Model):
    REASON_CHOICES = [
        ('spam', 'Spam or Misleading'),
        ('fraud', 'Fraud or Scam'),
        ('inappropriate', 'Inappropriate Content'),
        ('duplicate', 'Duplicate Listing'),
        ('other', 'Other'),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reports'
    )
    reporter = models.ForeignKey(
        UserCredential, on_delete=models.CASCADE, related_name='reports'
    )
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True, default='')
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Report on {self.product.title} by {self.reporter.username}"


class Transaction(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='transactions'
    )
    seller = models.ForeignKey(
        UserCredential, on_delete=models.CASCADE, related_name='sales'
    )
    buyer = models.ForeignKey(
        UserCredential, on_delete=models.CASCADE, related_name='purchases'
    )
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.product.title}: {self.seller.username} → {self.buyer.username}"