from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Custom User Model based on Django's default (username-based) auth
class User(AbstractUser):
    # Inherit everything from AbstractUser without any custom fields (can add custom fields here later if needed)
    pass

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"


# Order Model
class Order(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="orders")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("shipped", "Shipped"), ("delivered", "Delivered")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Automatically calculate total price before saving"""
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} - {self.customer.username}"


# Product Model (Updated for Image Upload)
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("shipped", "Shipped"), ("delivered", "Delivered")],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product {self.name} by {self.user.username}"
# models.py

class PaymentProof(models.Model):
    customer_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    order_summary = models.TextField()
    proof_file = models.FileField(upload_to="payment_proofs/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment by {self.customer_name} ({self.phone_number})"
