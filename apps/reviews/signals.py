from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import ProductReview

@receiver(post_save, sender=ProductReview)
@receiver(post_delete, sender=ProductReview)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    
    # Calculate new average and count
    reviews = product.reviews.all()
    count = reviews.count()
    
    if count > 0:
        avg = reviews.aggregate(Avg('rating'))['rating__avg']
        product.avg_rating = round(avg, 2)
        
        # We need to save the number of reviews to Product if a field exists handling that count. 
        # But wait! Does Product have `rating_count` field?
        # A quick check earlier didn't show rating_count explicitly, except in context use or other queries.
        # Let's save `avg_rating` first, and if `rating_count` exists we can set it via `hasattr`.
        if hasattr(product, 'rating_count'):
            product.rating_count = count
    else:
        product.avg_rating = 0.0
        if hasattr(product, 'rating_count'):
            product.rating_count = 0
            
    product.save()
