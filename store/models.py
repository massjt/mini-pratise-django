from django.db import models

class Customer(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(null=False, max_length=50)
    password = models.CharField(null=False, max_length=20)
    address = models.CharField(null=True, max_length=100)
    phone = models.CharField(null=True, max_length=20)
    birthday = models.DateField(null=True)

    class Meta:
        db_table = 'Customers'
        ordering = ['id']

class Goods(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=100)
    price = models.FloatField()
    description = models.CharField(null=True, max_length=200)
    address = models.CharField(null=True, max_length=100)
    cpu_brand = models.CharField(null=True, max_length=30)
    cpu_type = models.CharField(null=True, max_length=30)
    memory_capacity = models.CharField(null=True, max_length=30)
    hd_capacity = models.CharField(null=True, max_length=30)
    card_model = models.CharField(null=True, max_length=30)
    displaysize = models.CharField(null=True, max_length=30)
    image = models.CharField(null=True, max_length=100)

    class Meta:
        db_table = 'Goods'
        ordering = ['id']

class Orders(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    order_date = models.DateTimeField()
    status = models.IntegerField(default=1)
    total = models.FloatField()

    class Meta:
        db_table = 'Orders'
        ordering = ['id']

class OrderLineItem(models.Model):
    id = models.AutoField(primary_key=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total = models.FloatField(default=0.0)

    class Meta:
        db_table = 'OrderLineItems'
        ordering = ['id']