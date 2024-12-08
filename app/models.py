#file này tạo bảng trong csdl thông qua sqlite3
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE, related_name='sub_categories',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=50,null=True)    
    slug = models.SlugField(max_length=50,unique=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length=50,null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True,blank=False)
    image = models.ImageField(null=True,blank=True)
    detail = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    @property 
    def imageurl(self):
        try:
            url= self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    SĐT = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
       
    def __str__(self):
        return self.address 
    

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Product  # Import sản phẩm nếu cần

class Invoice(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_email = models.EmailField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)  # Thêm trường timestamp để lưu thời gian

    def __str__(self):
        return f"Invoice {self.id} - {self.customer_name or 'Guest'}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} - {self.quantity}"