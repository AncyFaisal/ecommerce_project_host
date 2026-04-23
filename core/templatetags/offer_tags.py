from django import template
from django.utils import timezone
from decimal import Decimal

register = template.Library()


@register.filter
def get_best_offer(product):
    """
    Get the best offer for a product (by highest discount amount).
    Checks both product offers and category offers.
    """
    best_discount_amount = Decimal('0')
    best_offer = None
    now = timezone.now()

    try:
        # 1. Product-specific offers
        for offer in product.product_offers.filter(
            is_active=True,
            valid_from__lte=now,
            valid_to__gte=now
        ):
            # Use a dummy price of 100 to compare relative discount strength
            discount, _ = offer.calculate_discount(Decimal('100'))
            if discount > best_discount_amount:
                best_discount_amount = discount
                best_offer = offer

        # 2. Category offers (M2M — category has category_offers reverse relation)
        if product.category:
            for offer in product.category.category_offers.filter(
                is_active=True,
                valid_from__lte=now,
                valid_to__gte=now
            ):
                discount, _ = offer.calculate_discount(Decimal('100'))
                if discount > best_discount_amount:
                    best_discount_amount = discount
                    best_offer = offer

    except Exception as e:
        print(f"Error in get_best_offer: {e}")
        return None

    return best_offer


@register.filter
def get_offer_discount(price, product):
    """Calculate the discount amount for a product at a given price."""
    try:
        price = Decimal(str(price))
        best_offer = get_best_offer(product)
        if best_offer:
            discount, _ = best_offer.calculate_discount(price)
            return discount
    except Exception as e:
        print(f"Error in get_offer_discount: {e}")
    return Decimal('0')


@register.filter
def get_offer_percent(product):
    """Return the discount percentage label for a product offer badge."""
    try:
        now = timezone.now()
        best_pct = Decimal('0')
        best_offer = None

        for offer in product.product_offers.filter(
            is_active=True, valid_from__lte=now, valid_to__gte=now
        ):
            if offer.discount_percentage > best_pct:
                best_pct = offer.discount_percentage
                best_offer = offer

        if product.category:
            for offer in product.category.category_offers.filter(
                is_active=True, valid_from__lte=now, valid_to__gte=now
            ):
                if offer.discount_percentage > best_pct:
                    best_pct = offer.discount_percentage
                    best_offer = offer

        if best_offer and best_offer.discount_percentage > 0:
            return int(best_offer.discount_percentage)
    except Exception as e:
        print(f"Error in get_offer_percent: {e}")
    return None


@register.filter
def calculate_discount_percentage(discounted_price, original_price):
    """Calculate discount percentage from two prices."""
    try:
        if original_price and original_price > 0:
            discount = ((original_price - discounted_price) / original_price) * 100
            return round(discount)
    except (TypeError, ValueError, ZeroDivisionError):
        pass
    return 0


@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return value


@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value


@register.filter
def floatformat(value, digits=0):
    try:
        return f"{float(value):.{digits}f}"
    except (ValueError, TypeError):
        return value
