from msilib.schema import CustomAction
from django.shortcuts import redirect, render
from .forms import AddProductForm, AddProductImageForm
from django.contrib import messages
from appUser.models import CustomUser, Order, Product
from .decorators import admin_only
from django.contrib import messages
from datetime import date, timedelta



# Create your views here.
@admin_only
def homePage(request):
    return render(request, 'admin/homepage.html')


@admin_only
def addProduct(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product has been added")
            return redirect("addProduct")

    context = {
        'form':AddProductForm,
    }
    return render(request, 'admin/addProduct.html', context)


@admin_only
def addProductImage(request):
    if request.method == "POST":
        form = AddProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product has been added")
            return redirect("addProductImage")
    context= {
        'form':AddProductImageForm
    }
    return render(request, "admin/addProdImage.html", context)


@admin_only
def productStatus(request):
    order_obj = Order.objects.all().order_by("-id")
    context = {
        "order_obj":order_obj
    }
    return render(request, "admin/prodStatus.html", context)


@admin_only
def manageProductStatus(request, orderid, id):
    order_obj = Order.objects.filter(order_id=orderid, id=id).first()
    if request.method == "POST":
        stat = request.POST.get("status")
        if stat == "Return Approved":
            order_obj.estimate_dd = date.today() + timedelta(days=3)
        elif stat == "Returned":
            order_obj.estimate_dd = date.today()
            user_obj = CustomUser.objects.get(email=order_obj.user.email)
            user_obj.wallet += order_obj.price
            user_obj.save()
        elif stat == "Delivered":
            order_obj.estimate_dd = date.today()
        order_obj.status = stat
        order_obj.save()
        return redirect('/admin/manage-product-status/' + order_obj.order_id + "/" + str(order_obj.id) + "/")
    context = {
        "order_obj":order_obj,
    }
    return render(request, 'admin/manageProdStatus.html', context)


@admin_only
def manageProduct(request):
    prod_obj = Product.objects.all()
    context = {
        "prod_obj":prod_obj
    }
    return render(request, "admin/manageProd.html", context)


@admin_only
def manageSingleProd(request, id):
    prod_obj = Product.objects.get(id=id)
    context = {
        "prod": prod_obj
    }
    return render(request, "admin/manageSingleProd.html", context)


@admin_only
def deleteProduct(request):
    if request.method == "POST":
        id = request.POST.get("prod_id")
        prod_obj = Product.objects.get(id=id)
        prod_obj.delete()
        return redirect("products")


@admin_only
def updateQuantity(request):
    if request.method == "POST":
        id = request.POST.get("prod_id")
        quantity = request.POST.get("quantity")
        prod_obj = Product.objects.get(id=id)
        prod_obj.quantity = quantity
        prod_obj.save()
        messages.success(request, "Quantity Updated")
        return redirect("/admin/manage-product/" + id + "/") 