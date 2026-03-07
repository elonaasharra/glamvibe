from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem


def shop_home(request):

    products = Product.objects.all()

    cart_count = 0

    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, completed=False).first()
        if order:
            cart_count = sum(item.quantity for item in order.items.all())

    return render(request, 'shop/shop_home.html', {
        'products': products,
        'cart_count': cart_count
    })


def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    order, created = Order.objects.get_or_create(
        user=request.user,
        completed=False
    )

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if not created:
        order_item.quantity += 1
        order_item.save()

    return redirect("shop:shop_home")

def cart_view(request):

    order = Order.objects.filter(user=request.user, completed=False).first()

    items = []
    if order:
        items = order.items.all()

    return render(request, "shop/cart.html", {
        "items": items
    })
def checkout(request):
    order = Order.objects.filter(user=request.user, completed=False).first()



def remove_from_cart(request, item_id):

    item = OrderItem.objects.get(id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("shop:cart")

