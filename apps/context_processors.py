# context_processors.py
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.sanjeri_models import Cart, Wishlist, ProductOffer, CategoryOffer, WalletTransaction, Wallet

User = get_user_model()

def wallet_balance(request):
    """Context processor that auto-creates wallet if missing"""
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {'wallet_balance': 0}
    try:
        wallet, created = Wallet.objects.get_or_create(
            user=request.user,
            defaults={'balance': 0}
        )
        return {'wallet_balance': wallet.balance}
    except Exception:
        return {'wallet_balance': 0}


def cart_and_wishlist_context(request):
    """Consolidated context processor for both cart and wishlist"""
    context = {
        'cart_item_count': 0, 'cart_items_count': 0,
        'wishlist_count': 0, 'wishlist_items_count': 0,
        'wishlist_product_ids': [], 'wishlist_variant_ids': [],
    }

    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return context
        # Cart count
        try:
            cart = Cart.objects.get(user=request.user)
            context['cart_item_count'] = cart.total_items
            context['cart_items_count'] = cart.total_items
        except Cart.DoesNotExist:
            context['cart_item_count'] = 0
            context['cart_items_count'] = 0
        
        # Wishlist count
        try:
            wishlist = Wishlist.objects.prefetch_related('items').get(user=request.user)
            context['wishlist_count'] = wishlist.total_items
            context['wishlist_items_count'] = wishlist.total_items
            context['wishlist_product_ids'] = list(wishlist.items.values_list('product_id', flat=True))
            context['wishlist_variant_ids'] = list(wishlist.items.values_list('variant_id', flat=True))
        except Wishlist.DoesNotExist:
            context['wishlist_count'] = 0
            context['wishlist_items_count'] = 0
            context['wishlist_product_ids'] = []
            context['wishlist_variant_ids'] = []
    else:
        context['cart_item_count'] = 0
        context['cart_items_count'] = 0
        context['wishlist_count'] = 0
        context['wishlist_items_count'] = 0
        context['wishlist_product_ids'] = []
        context['wishlist_variant_ids'] = []
    
    return context

def offer_context(request):
    """Add offer information to all templates"""
    try:
        now = timezone.now()
        active_product_offers = ProductOffer.objects.filter(
            is_active=True, valid_from__lte=now, valid_to__gte=now
        ).prefetch_related('products')
        active_category_offers = CategoryOffer.objects.filter(
            is_active=True, valid_from__lte=now, valid_to__gte=now
        ).select_related('category')
        return {
            'now': now,
            'active_product_offers': active_product_offers,
            'active_category_offers': active_category_offers,
        }
    except Exception:
        return {'now': timezone.now(), 'active_product_offers': [], 'active_category_offers': []}


def admin_context(request):
    if not hasattr(request, 'user') or not request.user.is_staff:
        return {}
    try:
        pending_refunds_count = WalletTransaction.objects.filter(
            transaction_type='REFUND', status='PENDING'
        ).count()
        return {'pending_refunds_count': pending_refunds_count}
    except Exception:
        return {}