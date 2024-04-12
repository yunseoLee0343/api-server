from django.shortcuts import render

from django.http import JsonResponse
from .models import Product
import requests

def get_starbucks_data(request):
    url = 'https://www.starbucks.co.kr/upload/json/menu/W0000171.js'
    response = requests.get(url)
    data = response.json()

    for item in data['list']:
        new_product = item['newicon'] == 'Y'
        product_name = item['product_NM']
        cate_name = item['cate_name']
        content = item['content']
        calories = item['kcal']
        sugars = item['sugars']
        protein = item['protein']
        caffeine = item['caffeine']
        fat = item['sat_fat']
        sodium = item['sodium']

        Product.objects.create(
            new_product=new_product,
            product_name=product_name,
            cate_name=cate_name,
            content=content,
            calories=calories,
            sugars=sugars,
            protein=protein,
            caffeine=caffeine,
            fat=fat,
            sodium=sodium
        )

    return JsonResponse({'message': 'Data fetched and saved successfully'})
