
# Legacy Models Registry to bridge imports during architecture transition
from apps.accounts.models import CustomUser, Address, ReferralCoupon, UserData
from apps.products.models import Product, ProductVariant, ProductImage, Category, HomeBrand, HomeCategory, HomeRating, HomeProduct, CategoryOffer, ProductOffer, OfferApplication
from apps.orders.models import Order, OrderItem
from apps.cart.models import Cart, CartItem
from apps.wishlist.models import Wishlist, WishlistItem
from apps.coupons.models import Coupon
from apps.wallet.models import Wallet, WalletTransaction
from apps.payments.models import PaymentTransaction
