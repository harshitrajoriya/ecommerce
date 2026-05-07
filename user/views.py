from django.shortcuts import render, redirect
from accounts.models import Product, Cart , Order, OrderItem
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,"index.html")

def userhome(request):
    if not request.user.is_authenticated:
        return redirect('login')
    products=Product.objects.all().order_by('id')
    
    paginator=Paginator(products,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,"userhome.html",{'products':page_obj})

def p_detail(request,id):
    product=Product.objects.get(id = id)
    return render(request,"p_detail.html",{'product':product})

def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.product_discount_price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request,id):
    product = Product.objects.get(id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    messages.success(request,"Item added to Cart")
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('userhome')

def remove_from_cart(request, id):
    Cart.objects.filter(id=id, user=request.user).delete()
    messages.success(request,"Item removed Successfully")
    return redirect('cart')

def place_order(request):
    items= Cart.objects.filter(user= request.user)
    total = sum(
        item.product.product_discount_price * item.quantity
        for item in items
    )
    order = Order.objects.create(
        user=request.user,
        total_price=total,
        status='pending'
    )
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.product_discount_price
        )
    items.delete()
    messages.success(request,"order placed")
    return redirect('order_placed')

def order_placed(request):
    
    return render(request,"order_placed.html")

