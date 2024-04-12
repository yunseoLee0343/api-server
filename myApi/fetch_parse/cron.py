from django.db import transaction
from django.http import JsonResponse
from django_cron import CronJobBase, Schedule
from .models import Product
import requests

class FetchStarbucksDataJob(CronJobBase):
    RUN_EVERY_MINS = 60 * 24  # 24시간마다 실행

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'myapp.fetch_starbucks_data_job'    # 고유 코드

    def do(self):
        urls = [
            'https://www.starbucks.co.kr/upload/json/menu/W0000171.js',
            'https://www.starbucks.co.kr/upload/json/menu/W0000060.js',
            'https://www.starbucks.co.kr/upload/json/menu/W0000003.js',
            'https://www.starbucks.co.kr/upload/json/menu/W0000004.js',
            'https://www.starbucks.co.kr/upload/json/menu/W0000005.js',
            'https://www.starbucks.co.kr/upload/json/menu/W0000422.js',
            'https://www.starbucks.co.kr/upload/json/menu/W0000061.js',
            'https://www.starbucks.co.kr/upload/json/menu/W0000075.js',
            'https://www.starbucks.co.kr/upload/json/menu/W0000053.js',
            'https://www.starbucks.co.kr/upload/json/menu/W0000062.js',
            'https://www.starbucks.co.kr/upload/json/menu/W0000480.js',
        ]

        for url in urls:
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

                with transaction.atomic():
                    # 모델에 데이터 추가
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
