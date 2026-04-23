from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.products.models import Product
from .models import ProductReview
from django.http import JsonResponse
import json

@login_required
def add_review(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id, is_active=True, is_deleted=False)
        
        try:
            # Handle both Form encoding and JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                rating = data.get('rating')
                comment = data.get('comment', '')
            else:
                rating = request.POST.get('rating')
                comment = request.POST.get('comment', '')
            
            if not rating:
                messages.error(request, "Please provide a rating.")
                return redirect('product_detail', product_id=product.id)
                
            rating = int(rating)
            if rating < 1 or rating > 5:
                messages.error(request, "Rating must be between 1 and 5.")
                return redirect('product_detail', product_id=product.id)
                
            # Check if user already reviewed
            review, created = ProductReview.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            
            # Update product aggregates
            all_reviews = ProductReview.objects.filter(product=product)
            count = all_reviews.count()
            avg = sum(r.rating for r in all_reviews) / count if count > 0 else 0.0
            
            product.rating_count = count
            product.avg_rating = round(avg, 2)
            product.save()
            
            if request.content_type == 'application/json':
                return JsonResponse({'status': 'success', 'message': 'Review submitted successfully!'})
                
            messages.success(request, "Thank you! Your review has been submitted.")
        except Exception as e:
            if request.content_type == 'application/json':
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            messages.error(request, f"Error submitting review: {e}")
            
        return redirect('product_detail', product_id=product.id)
    
    return redirect('homepage')
