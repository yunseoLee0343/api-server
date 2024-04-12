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
    imageUrl = models.URLField(max_length=100, default='https://image.istarbucks.co.kr/upload/store/skuimg/2021/04/[9200000002487]_20210426091745609.jpg')
