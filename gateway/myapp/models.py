from django.db import models


class Customer(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(unique=True)
  created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  order_date = models.DateTimeField(auto_now_add=True)
  total_price = models.DecimalField(max_digits=10, decimal_places=2)
