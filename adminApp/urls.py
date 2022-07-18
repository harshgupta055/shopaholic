
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name="adminHome"),
    path('add-product/', views.addProduct, name="addProduct"),
    path('add-product-image/', views.addProductImage, name="addProductImage"),
    path('product-status/', views.productStatus, name="productStatus"),
    path('products/', views.manageProduct, name="products"),
    path('manage-product/<int:id>/', views.manageSingleProd, name="manageProd"),
    path('manage-product-status/<str:orderid>/<int:id>/', views.manageProductStatus, name="manageProdStatus"),
    path('delete-product/', views.deleteProduct, name="deleteProduct"),
    path('update-quantity/', views.updateQuantity, name="updateQuantity"),

]