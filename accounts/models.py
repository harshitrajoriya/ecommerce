from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Adminprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.username

class Userprofile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    user_email=models.EmailField()
    
    def __str__(self):
        return self.user.username

class Product(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    product_name = models.CharField(max_length=100)
    product_title = models.CharField(max_length=200)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    product_image = models.ImageField(upload_to='products/')
    
    product_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    
    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity= models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
    
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped',   'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at   = models.DateTimeField(default=timezone.now)
    total_price  = models.DecimalField(max_digits=10, decimal_places=2)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price    = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"