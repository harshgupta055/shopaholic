

from datetime import date, timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.template.defaultfilters import slugify

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField(blank=True, null=True)
    wallet = models.FloatField(default=0.0, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()



class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, blank=True)
    about = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True, related_name="P_category")
    quantity = models.IntegerField(default=0)
    favourites = models.ManyToManyField(CustomUser, blank=True, related_name="user_favourite")
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to='product/', blank=True, default='product/noimage.jpg')
    avg_rating = models.FloatField(blank=True, default=0.0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)



class ProductRating(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="rating_prod")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rating_user")
    rating = models.IntegerField(blank=True)

    def __str__(self):
        return self.user.first_name


class ProductComments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True) 
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)


class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to='product/', blank=True)

    def __str__(self):
        return self.product.name



class Address(models.Model):
    STATE_CHOICES = [
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odissa', 'Odissa'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ]
    id = models.AutoField(primary_key=True) 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=50, blank=True)
    phone = models.BigIntegerField(blank=True)
    pin_code = models.IntegerField(blank=True)
    house = models.CharField(max_length=60, blank=True)
    area = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    default = models.BooleanField(default=False)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, blank=True)

    def __str__(self):
        return(self.house + ", " + self.area + ", " + self.city + ", " + self.state + ", " + str(self.pin_code))


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, default=1)

    def __str__(self):
        return self.user.first_name


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('Wallet', 'Wallet'),
        ('COD', 'COD')
    ]
    STATUS_CHOICES = [
        ('Getting Ready for Packing', 'Getting Ready for Packing'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Cancelled', 'Cancelled'),
        ('Delivered', 'Delivered'),
        ('Requested for Return', 'Requested for Return'),
        ('Return Approved', 'Return Approved'),
        ('Returned', 'Returned'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300, blank=True)
    price = models.FloatField(blank=True, null=True)
    prod_image = models.ImageField(upload_to='product/', blank=True, default='product/noimage.jpg')
    deliver_to = models.CharField(max_length=60, blank=True)
    phone = models.BigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, blank=True, default='Getting Ready for Packing')
    order_id = models.CharField(max_length=15, blank=True)
    payment_mode = models.CharField(max_length=10, blank=True, choices=PAYMENT_CHOICES)
    amount = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    estimate_dd = models.DateField(default=date.today() + timedelta(days=7))

    def __str__(self):
        return self.order_id


    def save(self, *args, **kwargs):  # new
        self.name = self.product.name
        self.price = self.product.price
        self.prod_image = self.product.image
        return super().save(*args, **kwargs)


class SearchHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title