from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login, logout
from accounts.models import Product, Order

# Create your views here.
def register_page(request):
    if request.method =="POST":
        user_full_name=request.POST.get("fullname")
        user_email    =request.POST.get("email")
        user_password =request.POST.get("password")
        user_cpassword=request.POST.get("confirm_password")
        
        if User.objects.filter(email=user_email).exists():
            messages.error(request,"email already registered")
            return redirect('register')
        
        if user_password != user_cpassword:
            messages.error(request,"password Didn't match")
            return redirect('register')
        user = User.objects.create_user(
            first_name=user_full_name,
            username=user_email,
            email =user_email,
            password=user_password,
        )
        return redirect('login')
    return render(request,"register.html")

def login_page(request):
    if request.method =="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        
        if not User.objects.filter(email=email).exists():
            messages.error(request,"invalid email")
            return redirect('login')
        # if not User.objects.filter(password=password).exists():
        #     messages.error(request,"wrong password")
        #     return redirect('login')
        
        user=authenticate(request,username=email,password=password)
        if user is None:
            messages.error(request, "Wrong password!")
            return redirect('login')
        login(request,user)
        return redirect ('userhome')
    return render(request,"login.html")


def adminhome(request):
    # if request.method == "POST":
    #     product_name            = request.POST.get("name")
    #     product_title           = request.POST.get("title")
    #     product_description     = request.POST.get("description")
    #     product_price           = request.POST.get("price")
    #     product_discount_price  = request.POST.get("discount_price")
    #     product_image           = request.FILES.get("image")
    #     product_status          = request.POST.get("status")
        
    #     product=Product.objects.create(
    #         product_name=product_name,
    #         product_title=product_title,
    #         product_description=product_description,
    #         product_price=product_price,
    #         product_discount_price=product_discount_price,
    #         product_image=product_image,
    #         product_status=product_status,
    #     )
    #     product.save()
    #     return redirect('adminhome')
    products=Product.objects.all()
    return render(request,"adminhome.html",{'products':products})

def delete_product(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    return redirect('adminhome')

def edit_product(request,id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.product_name            = request.POST.get("name")
        product.product_title           = request.POST.get("title")
        product.product_description     = request.POST.get("description")
        product.product_price           = request.POST.get("price")
        product.product_discount_price  = request.POST.get("discount_price")
        product.product_status          = request.POST.get("status")
        
        if request.FILES.get("image"):
            product.product_image = request.FILES.get("image")

        product.save()
        messages.success(request,"Product Updated")
        return redirect("adminhome")
    return render(request, "edit_product.html",{'product':product})

def logout_page(request):
    logout(request)
    return redirect('login')

def admin_add(request):
    if request.method == "POST":
        product_name            = request.POST.get("name")
        product_title           = request.POST.get("title")
        product_description     = request.POST.get("description")
        product_price           = request.POST.get("price")
        product_discount_price  = request.POST.get("discount_price")
        product_image           = request.FILES.get("image")
        product_status          = request.POST.get("status")
        
        if product_discount_price and float(product_discount_price) > float(product_price):
            messages.error(request,"discount price can't be greater than actual price")
            return redirect('admin_add')
        product=Product.objects.create(
            product_name=product_name,
            product_title=product_title,
            product_description=product_description,
            product_price=product_price,
            product_discount_price=product_discount_price,
            product_image=product_image,
            product_status=product_status,
        )
        product.save()
        messages.success(request,"Product Added Successfully")
        return redirect('admin_add')
    products=Product.objects.all()
    return render(request,'admin_add.html')

def toggle_status(request, id):
    product = Product.objects.get(id=id)
    if product.product_status == 'active':
        product.product_status = 'inactive'
    else:
        product.product_status = 'active'
    product.save()
    return redirect('adminhome')

def admin_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})