from django.db import models

# Create your models here.

class Registration(models.Model):
    first_name = models.CharField(max_length=50,null = True, blank=True)
    last_name = models.CharField(max_length=50,null = True, blank=True)
    email = models.CharField(max_length=60,null = True, blank=True)
    password = models.CharField(max_length=255,null = True, blank=True)
    mobile = models.BigIntegerField()
    gender = models.CharField(max_length=50,null = True, blank=True)


    def __str__(self):
        return self.first_name
    

#tables for categories

class Category(models.Model):
    cat_name = models.CharField(max_length=100,default="",null=True,blank=True)
    cat_image = models.ImageField(upload_to='Category/')

    def __str__(self):
        return self.cat_name
    
# table for product

class Product(models.Model):
    pro_name = models.CharField(max_length=100,default="",null=True,blank=True)
    pro_image = models.ImageField(upload_to='Product/')
    price = models.IntegerField(null=True,blank=True,default=0)
    desc = models.TextField(max_length=255,default="",null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.pro_name
    
# table for order

class Order(models.Model):
    address = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.BigIntegerField(null=True, blank=True, default=0)
    price = models.BigIntegerField(null=True, blank=True, default=0)
    customer = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.BigIntegerField(null=True, blank=True, default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product.pro_name
    
    


    

    