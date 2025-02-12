import stripe
from django.conf import settings

stripe.api_key = settings.STRIP_API_KEY


def create_product(course_name, description):
    """
    Создаёт продукт в Stripe.
    """
    product = stripe.Product.create(
        name=course_name,
        description=description
    )
    return product


def create_stripe_price(amount, product_id):
    """Создает цену в stripe"""

    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data=product_id,
    )
    return price


def create_stripe_session(price_id):
    """Создает сессию на оплату в stripe"""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
