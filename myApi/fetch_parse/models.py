from django.db import models

class Product(models.Model):
    new_product = models.BooleanField(default=False)
    product_name = models.CharField(max_length=100)
    cate_name = models.CharField(max_length=100)
    content = models.TextField()
    calories = models.IntegerField()
    sugars = models.IntegerField()
    protein = models.IntegerField()
    caffeine = models.IntegerField()
    fat = models.IntegerField()
    sodium = models.IntegerField()
