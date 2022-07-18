import random
import string
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from .forms import UserAdminCreationForm
from django.contrib import messages
from .models import CustomUser, Order, ProductImage, Product, Cart, Address, ProductComments, ProductRating, SearchHistory
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.db.models import Avg
from adminApp.decorators import admin_redirect
# Create your views here.


@admin_redirect
def home(request):
    prod_smart = Product.objects.filter(category__name="Smartphones").order_by("-id")[:5]
    prod_men_shirt = Product.objects.filter(category__name="Men Shirts").order_by("-id")[:5]
    context = {
        'prod': prod_smart,
        'prod_ms': prod_men_shirt,
    }
    return render(request, 'appUser/home.html', context)


# Authentication Views

def signup(request):
    signupform = UserAdminCreationForm()
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your account has been successfully created!')
            return redirect('login')
        else:
            messages.error(request, form.errors.as_text())
            return redirect('signup')
    context = {'form': signupform}
    return render(request, "appUser/signup.html", context)


@csrf_exempt
@api_view(["POST"])
def signupFormValid(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if CustomUser.objects.filter(email=email).first():
            return JsonResponse({"msg":"Email already taken", "field":"email"})
        elif CustomUser.objects.filter(phone=phone).first():
            return JsonResponse({"msg":"Phone number already registered!", "field":"phone"})
        elif len(str(phone)) != 10:
            return JsonResponse({"msg":"You must enter 10-digit phone number", "field":"phone"})
        elif password1 != password2:
            return JsonResponse({"msg":"Both password field must be same!", "field":"password2"})
        elif first_name.lower() in password1.lower():
            return JsonResponse({"msg":"Your password is too similar with the first name!", "field":"password1"})
        elif last_name.lower() in password1.lower():
            return JsonResponse({"msg":"Your password is too similar with the last name!", "field":"password1"})
        else:
            return JsonResponse({"msg":"ok", "field":"ok"})


def loginUser(request):
    if request.method == "POST":
        valuenxt = request.POST.get('next', None)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            if valuenxt:
                return redirect(valuenxt)
            return redirect('home')
        else:
            messages.error(request, 'Email or Password is incorrect!')
            return redirect('login')
    return render(request, "appUser/login.html")


@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required
@csrf_exempt
@api_view(["POST"])
def confirmPassword(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = authenticate(
            request, email=request.user.email, password=password)
        if user:
            return JsonResponse({"msg": "authenticated"})
        else:
            return JsonResponse({"msg": "Wrong Password"})


@login_required
@csrf_exempt
@api_view(["POST"])
def updatePassword(request):
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            return JsonResponse({"msg": "Both password fields must be same", "resp": "error"})
        user_obj = CustomUser.objects.get(email=request.user.email)
        user_obj.set_password(password1)
        user_obj.save()
        login(request, user_obj)
        return JsonResponse({"msg": "Password Changed", "resp": "success"})


# Personal Pages Views

@login_required
@csrf_exempt
@api_view(["POST", "GET"])
def profilePage(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        print(phone)
        user_obj = CustomUser.objects.filter(phone=int(phone)).first()
        if int(phone) == request.user.phone:
            pass
        elif len(str(phone)) != 10:
            return JsonResponse({"msg": "You must enter 10-digits number", "resp": "error"})
        elif user_obj:
            return JsonResponse({"msg": "This phone number is already registered", "resp": "error"})

        user_obj = CustomUser.objects.get(email=request.user.email)
        user_obj.phone = int(phone)
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.save()
        return JsonResponse({"msg": "Updated"})
    add_obj = Address.objects.filter(
        user_id=request.user.pk, default=True).first()
    context = {
        'add_obj': add_obj,
    }
    return render(request, 'appUser/profile.html', context)


@login_required
@csrf_exempt
@api_view(["POST"])
def add_balance(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        user_obj = CustomUser.objects.get(email=request.user.email)
        user_obj.wallet += float(amount)
        user_obj.save()
        return JsonResponse({"msg": "added"})


@login_required
@api_view(["GET"])
def check_balance(request):
    if request.method == "GET":
        total = request.GET.get("total")
        print(total)
        if request.user.wallet >= float(total):
            return JsonResponse({"msg": "ok"})
        else:
            return JsonResponse({"msg": "You don't have enough balance in your wallet."})


# Address Manage Views

@login_required
def my_addreses(request):
    address = Address.objects.filter(user_id=request.user.pk).order_by('-id')
    context = {
        'addresses': address,
    }
    return render(request, 'appUser/addresses.html', context)


@login_required
@csrf_exempt
@api_view(["PUT"])
def set_default_address(request):
    if request.method == "PUT":
        add_id = request.data.get("add_id")
        Address.objects.filter(user_id=request.user.pk).update(default=False)
        user_add_obj = Address.objects.filter(id=add_id).first()
        user_add_obj.default = True
        user_add_obj.save()
        return JsonResponse({"msg": "set"})


@login_required
@csrf_exempt
@api_view(["POST"])
def add_address(request):
    if request.method == "POST":
        name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        pin_code = request.POST.get("pincode")
        house = request.POST.get("house")
        area = request.POST.get("area")
        city = request.POST.get("city")
        state = request.POST.get("state")
        default = request.POST.get("default", False)
        add_obj_check = Address.objects.filter(user_id=request.user.pk).first()
        if add_obj_check:
            add_obj = Address(user_id=request.user.pk, name=name, phone=int(
                phone), pin_code=int(pin_code), house=house, area=area, city=city, state=state, default=default)
        else:
            add_obj = Address(user_id=request.user.pk, name=name, phone=int(
                phone), pin_code=int(pin_code), house=house, area=area, city=city, state=state, default=True)
        add_obj.save()
        return JsonResponse({"msg": "added"})


@csrf_exempt
@api_view(["DELETE"])
def deleteAddress(request):
    if request.method == "DELETE":
        id = request.data.get("id")
        add_obj = Address.objects.filter(id=int(id))
        add_obj.delete()
        return JsonResponse({"msg":"deleted"})


# Orders Manage Views 

@login_required
def my_orders(request):
    orders = Order.objects.filter(user_id=request.user.pk).order_by("-id")
    context = {
        'orders': orders,
    }
    return render(request, 'appUser/myOrders.html', context)


@login_required
def orderStatus(request, orderid):
    order_obj = Order.objects.filter(order_id=orderid).first()
    context = {
        'order_obj':order_obj
    }
    return render(request, 'appUser/orderStatus.html', context)


@login_required
def cancelOrder(request):
    if request.method == "POST":
        ord_id = request.POST.get("order_id")
        ord_obj = Order.objects.get(order_id=ord_id)
        prod_obj = Product.objects.get(product_id=ord_obj.pro)
        ord_obj.status = "Cancelled"
        user_obj = CustomUser.objects.get(email=request.user.email)
        user_obj.wallet += ord_obj.price
        ord_obj.save()
        user_obj.save()
        return redirect("/view-order-status/" + ord_id + "/")


@login_required
def returnOrder(request):
    if request.method == "POST":
        ord_id = request.POST.get("order_id")
        ord_obj = Order.objects.get(order_id=ord_id)
        ord_obj.status = "Requested for Return"
        ord_obj.save()
        return redirect("/view-order-status/" + ord_id + "/")


# Wishlist views

@login_required
def wishlistPage(request):
    prod = Product.objects.filter(favourites__id=request.user.pk)
    context = {
        'prod': prod,
    }
    return render(request, "appUser/wishlist.html", context)


@login_required
@csrf_exempt
@api_view(["POST"])
def add_to_favourite(request):
    if request.method == "POST":
        prod_id = request.POST.get("prod_id")
        prod_obj = Product.objects.get(id=prod_id)
        if request.user not in prod_obj.favourites.all():
            prod_obj.favourites.add(request.user)
            return JsonResponse({"msg": "added to favourite"})
        else:
            prod_obj.favourites.remove(request.user)
            return JsonResponse({"msg": "removed from favourite"})


# Cart Views

@login_required
@csrf_exempt
@api_view(["POST"])
def addToCart(request):
    if request.method == "POST":
        id = request.POST.get('id')
        cart_obj = Cart.objects.filter(
            user_id=request.user.pk, product_id=id).first()
        if cart_obj:
            if cart_obj.quantity >= 5:
                return JsonResponse({"msg": "You can only add 5 quantity per item"})
            else:
                cart_obj.quantity += 1
                if cart_obj.product.quantity >= cart_obj.quantity:
                    cart_obj.save()
        else:
            cart_obj = Cart(user_id=request.user.pk, product_id=id)
            cart_obj.save()
        return JsonResponse({"msg": "added"})


@login_required
@csrf_exempt
@api_view(["DELETE"])
def removeFromCart(request):
    if request.method == "DELETE":
        id = request.data.get("id")
        Cart.objects.filter(product_id=id).delete()
        return JsonResponse({"msg": "Deleted"})


@login_required
def cartPage(request):
    cart_obj = Cart.objects.filter(user=request.user)
    total_price = 0
    for c in cart_obj:
        total_price += c.quantity*(c.product.price)
    context = {
        "items": cart_obj,
        'total_price': total_price
    }
    return render(request, 'appUser/cartitem.html', context)


@login_required
@csrf_exempt
def add_quantity(request):
    if request.method == "POST":
        id = request.POST.get("id")
        quantity = request.POST.get("quantity")
        cart_obj = Cart.objects.filter(id=int(id)).first()
        prod_obj = Product.objects.filter(id=cart_obj.product_id).first()
        if prod_obj.quantity >= int(quantity):
            cart_obj.quantity = int(quantity)
            cart_obj.save()
            return JsonResponse({"msg": "added"})
        return JsonResponse({"msg":"not added"})


@login_required()
def proceedToBuy(request):
    cart_obj = Cart.objects.filter(user=request.user)
    user_add = Address.objects.filter(user_id=request.user.pk)
    default_add = Address.objects.filter(
        user_id=request.user.pk, default=True).first()
    total_price = 0
    for c in cart_obj:
        total_price += c.quantity*(c.product.price)
    context = {
        "items": cart_obj,
        'total_price': total_price,
        'user_add': user_add,
    }
    return render(request, 'appUser/proceedToBuy.html', context)


@login_required
def choose_payment(request):
    if request.method == "GET":
        add_id = request.GET.get("address")
        cart_obj = Cart.objects.filter(user=request.user)
        default_add = Address.objects.filter(id=int(add_id), user_id=request.user.pk).first()
        total_price = 0
        for c in cart_obj:
            total_price += c.quantity*(c.product.price)
        context = {
            "items": cart_obj,
            'total_price': total_price,
            'default_add': default_add
        }
        return render(request, 'appUser/choosePayment.html', context)


@login_required
def order_confirmed(request):
    if request.method == "POST":
        payment = request.POST.get("mode")
        add_id = request.POST.get("add_id")
        ordered = []
        cart_obj = Cart.objects.filter(user=request.user)
        user_obj = CustomUser.objects.get(email=request.user.email)
        add_obj = Address.objects.filter(id=int(add_id)).first()
        total_price = 0
        for c in cart_obj:
            total_price += c.quantity*(c.product.price)
        for i in cart_obj:
            while True:
                order_id = ''.join(random.choices(
                    string.ascii_uppercase + string.digits, k=10))
                order_id = "SH" + order_id
                ord = Order.objects.filter(order_id=order_id).first()
                if not ord:
                    break
            order_obj = Order(user_id=request.user.pk, product_id=i.product.id, deliver_to=add_obj.name, phone=add_obj.phone, address=add_obj,
                              order_id=order_id, payment_mode=payment, amount=(i.quantity*i.product.price), quantity=i.quantity)
            prod_obj = Product.objects.filter(id=i.product.id).first()
            prod_obj.quantity -= i.quantity
            if prod_obj.quantity < 0:
                return HttpResponse("This product has been sold!")
            prod_obj.save()
            order_obj.save()
            ordered.append(order_obj)
        cart_obj.delete()
        user_obj.wallet -= total_price
        user_obj.save()
        context = {
            'order_obj': ordered,
            'payment_mode': payment,
            'total_price': total_price,
            'default_add': add_obj,
        }
        return render(request, 'appUser/orderConfirmed.html', context)


#Search Views

def searchResponse(request):
    if request.method == "GET":
        d = request.GET.get("data", None)
        prod = Product.objects.filter(name__icontains=d)[:8].values("name", "slug")
        return JsonResponse({"msg":list(prod)})


def searchHistory(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            sh = SearchHistory.objects.filter(user_id=request.user.pk).order_by("id")[:5].values("title")
            return JsonResponse({"msg":list(sh)})
        else:
            return JsonResponse({"msg":"No"})


@csrf_exempt
def saveSearchHistory(request):
    if request.method == "POST":
        d = request.POST.get("data")
        print(d)
        if request.user.is_authenticated:
            sf = SearchHistory.objects.filter(user_id=request.user.pk, title=d).first()
            if not sf:
                sf = SearchHistory(user_id=request.user.pk, title=d)
                sf.save()
        return JsonResponse({"mag":"History Saved"}) 


def searchPage(request):
    if request.method == "GET":
        d = request.GET.get("search")
        if request.user.is_authenticated:
            sf = SearchHistory.objects.filter(user_id=request.user.pk, title=d).first()
            if not sf:
                sf = SearchHistory(user_id=request.user.pk, title=d)
                sf.save()
        prod_obj = Product.objects.filter(name__icontains=d)
        context = {
            "sf":prod_obj
        }
        return render(request, "appUser/searchPage.html", context)


# Product Views

def categoryProduct(request, category):
    category = " ".join(category.split("-"))
    prod_obj = Product.objects.filter(category__name=category).order_by("-avg_rating")
    context = {
        "prod": prod_obj,
        "category": category
    }
    return render(request, "appUser/categoryProduct.html", context)



@csrf_exempt
@api_view(["POST"])
def add_review(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"msg":"no"})
        prod_id = request.POST.get("prod_id")
        comment = request.POST.get("comment")
        pc = ProductComments(user_id=request.user.pk,
                             product_id=prod_id, comment=comment)
        pc.save()
        return JsonResponse({"msg": "added"})



@csrf_exempt
@api_view(["POST"])
def rateProduct(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"msg": "Please login to rate product!"})
        id = request.POST.get("prod_id")
        rating = request.POST.get("rating")
        pr_obj = ProductRating.objects.filter(user_id=request.user.pk, product_id=id).first()
        if not pr_obj:
            pr_obj = ProductRating(user_id=request.user.pk,
                                product_id=id, rating=int(rating))
            pr_obj.save()
            avg = ProductRating.objects.filter(product_id=id).aggregate(Avg("rating"))
            prod = Product.objects.get(id=id)
            prod.avg_rating = round(avg["rating__avg"], 1)
            prod.save()
        return JsonResponse({"msg": "Rated"})


def productPage(request, name):
    prod_obj = Product.objects.filter(slug=name).first()
    if not prod_obj:
        return HttpResponse("This product has been removed from our app.")
    prod_comments = ProductComments.objects.filter(
        product=prod_obj).order_by("-id")
    prod_rating = ProductRating.objects.filter(
        user_id=request.user.pk, product=prod_obj).first()
    avg_rating = ProductRating.objects.filter(
        product=prod_obj).aggregate(Avg("rating"))
    total = ProductRating.objects.filter(product=prod_obj).count()
    prod_img = ProductImage.objects.filter(product_id=prod_obj)
    context = {
        'prod': prod_obj,
        'prod_img': prod_img,
        'prod_comments': prod_comments,
        'prod_rating': prod_rating,
        'remain': 5-(prod_rating.rating if prod_rating else 0),
        'total': total,
    }
    return render(request, 'appUser/product.html', context)

