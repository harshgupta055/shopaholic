
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', include("adminApp.urls")),

    # authentication APIs
    path('signup/', views.signup, name="signup"),
    path('validation-signup/', views.signupFormValid, name="signupValid"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('confirm-password/', views.confirmPassword, name="confirmPassword"),
    path('password-update/', views.updatePassword, name="updatePassword"),

    # personal pages APIs
    path('profile/', views.profilePage, name="profile"),
    path('add-balance/', views.add_balance, name="addBalance"),
    path('check-balance/', views.check_balance, name="checkBalance"),

    # address manage APIs
    path('my-addresses/', views.my_addreses, name="myAddresses"),
    path('set-default-address/', views.set_default_address),
    path('add-new-address/', views.add_address, name="addAddress"),
    path('delete-address/', views.deleteAddress, name="deleteAddress"),

    # orders manage APIs
    path('my-orders/', views.my_orders, name="myOrders"),
    path('view-order-status/<str:orderid>/', views.orderStatus, name="orderStatus"),
    path('cancel-order/', views.cancelOrder, name="cancelOrder"),
    path('return-order/', views.returnOrder, name="returnOrder"),

    # Wishlist APIs
    path('wish-list/', views.wishlistPage, name="wishlistPage"),
    path('add-to-favourite/', views.add_to_favourite, name="addToFavourite"),

    # cart APIs
    path('add-to-cart/', views.addToCart, name="addToCart"),
    path('remove-from-cart/', views.removeFromCart, name="removeFromCart"),
    path('cart/', views.cartPage, name="cartPage"),
    path('add-qantity/', views.add_quantity, name="addQuantity"),
    path('proceed-to-buy/', views.proceedToBuy, name="proceedToBuy"),
    path('choose-payment/', views.choose_payment, name="choosePayment"),
    path('confirm-order/', views.order_confirmed, name="orderConfirm"),

    # search APIs
    path('search-show/', views.searchResponse, name="searchResponse"),
    path('search-history-save/', views.saveSearchHistory, name="saveSearch"),
    path('get-search-history/', views.searchHistory, name="searchHistory"),
    path('search/', views.searchPage, name="searchPage"),

    # Product APIs
    path('category/<str:category>/', views.categoryProduct, name="categoryProduct"),
    path('add-review/', views.add_review, name="addReview"),
    path('add-rating/', views.rateProduct, name="rateProduct"),
    path('view-product/<str:name>/', views.productPage, name="ProductPage"),

]