import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from django.db.models import Q
from django.template.loader import render_to_string 

from apps.sanjeri_models import Wishlist, WishlistItem, Product, Category, ProductVariant, Cart, CartItem

@login_required
def wishlist_view(request):
    """Display the user's wishlist with search and filter"""
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_items = WishlistItem.objects.filter(
            wishlist=wishlist,
            product__is_active=True,
            product__is_deleted=False,
            product__category__is_active=True,
            product__category__is_deleted=False,
            variant__is_active=True,
            variant__stock__gt=0,
            variant__is_deleted=False
        ).select_related('product__category')
        
        all_categories = Category.objects.filter(is_active=True)
        
        search_query = request.GET.get('search', '')
        if search_query:
            wishlist_items = wishlist_items.filter(
                Q(product__name__icontains=search_query) |
                Q(product__description__icontains=search_query) |
                Q(product__brand__icontains=search_query) |
                Q(product__fragrance_type__icontains=search_query)
            )
        
        category_id = request.GET.get('category', '')
        if category_id:
            wishlist_items = wishlist_items.filter(product__category_id=category_id)
        
        gender = request.GET.get('gender', '')
        if gender:
            wishlist_items = wishlist_items.filter(product__variants__gender=gender)
        
        all_genders = ProductVariant.objects.filter(
            product__is_active=True, is_active=True
        ).values_list('gender', flat=True).distinct()
        
        if request.GET.get('ajax') == '1':
            html = render_to_string('wishlist_items_partial.html', {
                'wishlist_items': wishlist_items,
                'wishlist': wishlist,
            }, request=request)
            
            return JsonResponse({
                'html': html,
                'count': wishlist_items.count()
            })
        
        context = {
            'wishlist': wishlist,
            'wishlist_items': wishlist_items,
            'all_categories': all_categories,
            'search_query': search_query,
            'selected_category': int(category_id) if category_id else '',
            'selected_gender': gender,
            'available_genders': sorted(set(all_genders)),
        }
        return render(request, 'wishlist.html', context)
        
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(user=request.user)
        all_genders = Product.objects.filter(is_active=True).values_list('gender', flat=True).distinct()
        
        context = {
            'wishlist': wishlist,
            'wishlist_items': [],
            'all_categories': Category.objects.filter(is_active=True),
            'search_query': '',
            'selected_category': '',
            'selected_gender': '',
            'available_genders': sorted(set(all_genders)),
        }
        return render(request, 'wishlist.html', context)

@login_required
@require_http_methods(["POST"])
def add_to_wishlist(request, variant_id):
    """Add product variant to wishlist"""
    try:
        variant = get_object_or_404(ProductVariant, id=variant_id, is_active=True, is_deleted=False)
        product = variant.product
        
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        wishlist_item, item_created = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            variant=variant,
            defaults={'product': product}
        )
        
        wishlist_items_count = WishlistItem.objects.filter(wishlist=wishlist).count()
        
        if item_created:
            message = "Added to wishlist!"
            success = True
        else:
            message = "Already in your wishlist."
            success = False
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': success,
                'message': message,
                'wishlist_count': wishlist_items_count
            })
        
        if item_created:
            messages.success(request, message)
        else:
            messages.info(request, message)
        
        referer = request.META.get('HTTP_REFERER', 'homepage')
        return redirect(referer)
        
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': f"Error: {str(e)}"})
        messages.error(request, f"Error adding to wishlist: {str(e)}")
        return redirect('wishlist')

@login_required
@require_http_methods(["POST", "DELETE"])
def remove_from_wishlist(request, variant_id):
    """Remove variant from wishlist"""
    try:
        wishlist_item = WishlistItem.objects.filter(
            wishlist__user=request.user,
            variant_id=variant_id
        ).first()
        
        if not wishlist_item:
            return JsonResponse({'success': False, 'message': 'Item not found in wishlist'})
        
        product_name = str(wishlist_item.product)
        wishlist = wishlist_item.wishlist
        wishlist_item.delete()
        
        wishlist_items_count = WishlistItem.objects.filter(wishlist=wishlist).count()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"Removed from wishlist.",
                'wishlist_count': wishlist_items_count
            })
        
        messages.success(request, f"Removed from wishlist.")
        return redirect('wishlist')
        
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': f"Error: {str(e)}"})
        messages.error(request, f"Error removing item from wishlist: {str(e)}")
        return redirect('wishlist')

@login_required
def get_wishlist_count(request):
    """Get wishlist item count for AJAX requests"""
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        count = WishlistItem.objects.filter(wishlist=wishlist).count()
        return JsonResponse({'count': count})
    except Wishlist.DoesNotExist:
        return JsonResponse({'count': 0})

@login_required
def check_wishlist_status(request, variant_id):
    """Check if variant is in user's wishlist"""
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        in_wishlist = WishlistItem.objects.filter(
            wishlist=wishlist, 
            variant_id=variant_id
        ).exists()
        
        return JsonResponse({
            'in_wishlist': in_wishlist,
            'variant_id': variant_id
        })
    except Wishlist.DoesNotExist:
        return JsonResponse({'in_wishlist': False, 'variant_id': variant_id})

@login_required
def wishlist_count(request):
    """Get current wishlist count"""
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        count = wishlist.total_items
    except Wishlist.DoesNotExist:
        count = 0
    return JsonResponse({'count': count})

@login_required
def get_wishlist_item_id(request, variant_id):
    """Get wishlist item ID for a variant"""
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_item = WishlistItem.objects.get(wishlist=wishlist, variant_id=variant_id)
        return JsonResponse({'item_id': wishlist_item.id})
    except (Wishlist.DoesNotExist, WishlistItem.DoesNotExist):
        return JsonResponse({'item_id': None})

@login_required
@require_POST
@transaction.atomic
def add_to_cart_from_wishlist(request, variant_id):
    """Add product variant to cart and remove from wishlist in one operation"""
    try:
        variant = get_object_or_404(ProductVariant, id=variant_id, is_active=True, is_deleted=False)
        product = variant.product
        
        if variant.stock <= 0:
            return JsonResponse({'success': False, 'message': 'Variant not in stock'})
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant,
            defaults={'quantity': 1}
        )
        
        if not item_created:
            if cart_item.can_increment:
                cart_item.quantity += 1
                cart_item.save()
                message = "Quantity updated in cart!"
            else:
                message = "Maximum quantity reached!"
        else:
            message = "Added to cart!"
        
        removed = False
        try:
            wishlist_item = WishlistItem.objects.filter(
                wishlist__user=request.user,
                variant=variant
            ).first()
            if wishlist_item:
                wishlist_item.delete()
                removed = True
        except Exception:
            pass
        
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': cart.total_items,
            'wishlist_count': WishlistItem.objects.filter(wishlist__user=request.user).count(),
            'removed_from_wishlist': removed,
            'variant_id': variant.id,
            'product_name': product.name
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Error: {str(e)}"})

@login_required
@require_http_methods(["POST"])
def check_multiple_wishlist(request):
    """Check multiple variants in wishlist at once"""
    try:
        data = json.loads(request.body)
        variant_ids = data.get('variant_ids', [])
        
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_variant_ids = set(
            WishlistItem.objects.filter(
                wishlist=wishlist,
                variant_id__in=variant_ids
            ).values_list('variant_id', flat=True)
        )
        
        result = {str(vid): vid in wishlist_variant_ids for vid in variant_ids}
        result['total_count'] = WishlistItem.objects.filter(wishlist=wishlist).count()
        
        return JsonResponse(result)
    except Wishlist.DoesNotExist:
        result = {str(vid): False for vid in variant_ids}
        result['total_count'] = 0
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)