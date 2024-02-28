from django.conf import settings
from django.shortcuts import redirect

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def toggle_like(like):
    if like.is_active:
        like.is_active = False
        like.save()
    else:
        like.is_active = True
        like.save()


def toggle_dislike(dislike):

    if dislike.is_active:
        dislike.is_active = False
        dislike.save()
    else:
        dislike.is_active = True
        dislike.save()


def create_product(instance):
    product = stripe.Product.create(name=f"{instance.username}")
    return product


def create_price(instance):
    product = create_product(instance)
    price = stripe.Price.create(
        unit_amount=100,
        currency="usd",
        recurring={"interval": "month"},
        product=f"{product.id}",
    )
    return price


def create_session(instance):
    price = create_price(instance)
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": f"{price.id}",
                "quantity": 1,
            },
        ],
        mode="subscription",
        success_url=f"http://127.0.0.1:8000/user/subscribe/{instance.pk}",
        cancel_url=f"http://127.0.0.1:8000/user/profile/{instance.pk}",
    )

    return redirect(checkout_session.url, code=303)
