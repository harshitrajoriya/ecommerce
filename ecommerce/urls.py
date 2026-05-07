"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import login_page, register_page, logout_page,adminhome,delete_product,edit_product,admin_add,toggle_status,admin_orders
from user.views import index, userhome,p_detail,cart_page,add_to_cart, remove_from_cart,place_order,order_placed
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('login/',login_page,name="login"),
    path('register/',register_page,name="register"),
    path('userhome/',userhome,name="userhome"),
    path('logout/',logout_page,name='logout'),
    path('adminhome/',adminhome,name='adminhome'),
    path('delete-product/<int:id>/',delete_product,name="delete_product"),
    path('edit-product/<int:id>/',edit_product,name="edit_product"),
    path('p_details/<int:id>/',p_detail,name="p_details"),
    path('cart/',cart_page,name="cart"),
    path('add-to-cart/<int:id>/',add_to_cart,name="add_to_cart"),
    path('remove-from-cart/<int:id>/',remove_from_cart,name="remove_from_cart"),
    path('admin-add/',admin_add,name="admin_add"),
    path('toggle-status/<int:id>/', toggle_status, name='toggle_status'),
    path('place-order/',place_order,name="place_order"),
    path('order-placed/',order_placed,name="order_placed"),
    path('admin-orders/',                   admin_orders,         name='admin_orders'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
