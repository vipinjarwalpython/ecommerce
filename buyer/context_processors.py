
from .models import CartItem


def cart_item_count(request):
    user = request.user
    if user.is_authenticated:
        cart_item_count = 0
        cart = CartItem.objects.filter(user_id=user.id)
        for c in cart:
            cart_item_count = cart_item_count + c.quantity

    else:
        cart_item_count = 0

    return {"cart_item_count": cart_item_count}
