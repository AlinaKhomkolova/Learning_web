import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY  # Подключение API ключа


def create_product(name, description):
    """Создает продукт в Stripe"""
    try:
        product = stripe.Product.create(name=name, description=description)
        return product.id
    except stripe.error.StripeError as e:
        print(f'Ошибка при создании продукта {e}')
        return None


def create_price(amount, product_id):
    """Создает цену продукта"""
    try:
        price = stripe.Price.create(
            unit_amount=amount * 100,
            currency='pln',
            product=product_id
        )
        return price.id
    except stripe.error.StripeError as e:
        print(f'Ошибка при создании прайса {e}')
        return None


def create_checkout_session(price_id):
    """Создает сессию оплаты в Stripe"""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
            success_url="https://127.0.0.1:8000/",
        )
        return session.id, session.url

    except stripe.error.StripeError as e:
        print(f"Ошибка при создании сессии: {e}")
    return None, None
