# views/homepage.py
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from apps.products.models import Product, ProductVariant
from apps.cart.models import Cart, CartItem
from apps.wishlist.models import Wishlist, WishlistItem


def homepage(request):
    """Home page view with actual products and search functionality"""
    query = request.GET.get('q', '')
    
     # Get all active, in-stock products with active categories
    all_products = Product.objects.filter(
        is_active=True, 
        is_deleted=False,
        category__is_active=True,
        category__is_deleted=False,
        variants__is_active=True,
        variants__stock__gt=0,
        variants__is_deleted=False
    ).distinct()
    cart_item_count = 0
    
    # Get wishlist product IDs for authenticated user
    wishlist_product_ids = []
    wishlist_variant_ids = []
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item_count = cart.total_items
        except Cart.DoesNotExist:
            pass
        
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_product_ids = list(WishlistItem.objects.filter(wishlist=wishlist).values_list('product_id', flat=True))
            wishlist_variant_ids = list(WishlistItem.objects.filter(wishlist=wishlist).values_list('variant_id', flat=True))
        except Wishlist.DoesNotExist:
            wishlist_variant_ids = []
    
    # Apply search filter if query exists
    if query:
        search_products = all_products.filter(
            Q(name__icontains=query) | 
            Q(brand__icontains=query) |
            Q(description__icontains=query) |
            Q(fragrance_type__icontains=query)
        )
        is_searching = True
        search_results_count = search_products.count()
    else:
        search_products = None
        is_searching = False
        search_results_count = 0

    # Get featured products (only show if not searching)
    if not is_searching:
        featured_products = all_products.filter(is_featured=True)[:8]
    else:
        featured_products = search_products[:8] if search_products else []
    
    # Get products by gender for different sections
    mens_products = all_products.filter(
        variants__gender="Male",
        variants__is_active=True
    ).distinct()[:4]
    
    womens_products = all_products.filter(
        variants__gender="Female", 
        variants__is_active=True
    ).distinct()[:4]
    
    unisex_products = all_products.filter(
        variants__gender="Unisex", 
        variants__is_active=True
    ).distinct()[:4]

    # Add is_in_wishlist attribute to each product
    for product in featured_products:
        product.is_in_wishlist = product.id in wishlist_product_ids
    
    for product in mens_products:
        product.is_in_wishlist = product.id in wishlist_product_ids
    
    for product in womens_products:
        product.is_in_wishlist = product.id in wishlist_product_ids
    
    for product in unisex_products:
        product.is_in_wishlist = product.id in wishlist_product_ids

    context = {
        'title': 'Home - Sanjeri',
        'featured_products': featured_products,
        'mens_products': mens_products,
        'womens_products': womens_products,
        'unisex_products': unisex_products,
        'user': request.user,
        'search_query': query,
        'is_searching': is_searching,
        'search_results_count': search_results_count,
        'search_products': search_products,
        'cart_item_count': cart_item_count,
        'wishlist_product_ids': wishlist_product_ids,
        'wishlist_variant_ids': wishlist_variant_ids,
        # 'wishlist_product_ids': list(wishlist_items),
    }
    return render(request, 'homepage.html', context)

