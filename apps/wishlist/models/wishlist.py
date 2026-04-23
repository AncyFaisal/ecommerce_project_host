# models/wishlist.py
from django.db import models
from django.conf import settings
from apps.products.models import Product, ProductVariant

# models/wishlist.py - Add this method to Wishlist model
class Wishlist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='wishlist'
    )
    products = models.ManyToManyField(Product, through='WishlistItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"
    
    @property
    def total_items(self):
        """Count items in wishlist"""
        return self.items.count()

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist, 
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['wishlist', 'variant']
        
    def __str__(self):
        return f"{self.variant} in {self.wishlist}"