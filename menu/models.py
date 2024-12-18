from django.db import models
from authentication.models import User  # Ensure you import User from the right location

class VegMenu(models.Model):
    FOOD_TYPES = [
        ('briyani', 'Briyani'),
        ('meals', 'Meals'),
        ('starters', 'Starters'),
        ('variety rice', 'Variety Rice'),
        ('dosa', 'Dosa'),
        ('rotti', 'Rotti'),
        ('gravies', 'Gravies'),
        ('cold beverages', 'Cold Beverages'),
        ('hot beverages', 'Hot Beverages'),
        ('snacks', 'Snacks'),
        ('ice cream', 'Ice Cream'),
    ]
    name = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=140, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    picture = models.ImageField(upload_to='picture/', null=True)
    food_type = models.CharField(max_length=50, choices=FOOD_TYPES, default="briyani")

    def __str__(self):
        return self.name

class NonVegMenu(models.Model):
    FOOD_TYPES = [
        ('nv briyani', 'Non Veg Briyani'),
        ('nv meals', 'Non Veg Meals'),
        ('nv starters', 'Non Veg Starters'),
        ('nv fried rice', 'Non Veg Fried Rice'),
        ('nv dosa', 'Non Veg Dosa'),
        ('nv rotti', 'Non Veg Rotti'),
        ('nv gravies', 'Non Veg Gravies'),
        ('nv snacks', 'Non Veg Snacks'),
    ]
    name = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=140, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    picture = models.ImageField(upload_to='picture/', null=True)
    food_type = models.CharField(max_length=50, choices=FOOD_TYPES, default="nv briyani")

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    handling_fee = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    gst = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    address = models.CharField(null=True, max_length=255)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="cart_items")
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.quantity})"
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address", null=True)
    street = models.CharField(null=True, max_length=50)
    address_line_1 = models.CharField(max_length=255, null=True)
    address_line_2 = models.CharField(max_length=255, null=True)
    state = models.CharField(null=True, max_length=50)
    


