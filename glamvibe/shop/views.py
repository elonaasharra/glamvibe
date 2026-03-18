from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, Category
from django.http import JsonResponse

def shop_home(request):

    products = Product.objects.all()
    categories = Category.objects.all()

    category_slug = request.GET.get("category")

    if category_slug:
        products = products.filter(categories__slug=category_slug)

    cart_count = 0

    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, completed=False).first()
        if order:
            cart_count = sum(item.quantity for item in order.items.all())

    return render(request, 'shop/shop_home.html', {
        'products': products,
        'categories': categories,
        'cart_count': cart_count
    })

from django.http import JsonResponse

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

    cart_count = sum(item.quantity for item in order.items.all())

    return JsonResponse({
        "cart_count": cart_count
    })
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

def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug)

    cart_count = 0

    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, completed=False).first()

        if order:
            cart_count = sum(item.quantity for item in order.items.all())

    return render(request, "shop/product_detail.html", {
        "product": product,
        "cart_count": cart_count
    })