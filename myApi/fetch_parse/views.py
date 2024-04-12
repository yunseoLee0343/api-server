# views.py
from django.core.serializers import serialize
from django.db import transaction
from django.http import JsonResponse
from .models import Product
from django.core.exceptions import ObjectDoesNotExist
import requests
import queue
import threading

# 우선순위 큐 생성
priority_queue = queue.PriorityQueue()

def parse_float(value):
    if '.' in value:
        temp = value.split('.')[0];
        if temp != '':
            return int(temp)
        else:
            return 0
    else:
        return int(value)

# 크롤링 작업 함수
def fetch_and_save_starbucks_data():
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
            cate_name = item['cate_NAME']
            content = item['content']
            calories = parse_float(item['kcal'])
            sugars = parse_float(item['sugars'])
            protein = parse_float(item['protein'])
            caffeine = parse_float(item['caffeine'])
            fat = parse_float(item['sat_FAT'])
            sodium = parse_float(item['sodium'])
            image_path = 'https://image.istarbucks.co.kr/' + item['file_PATH']

            # 우선순위 설정
            priority = 1 if response.status_code == 200 else 0

            # 우선순위 큐에 작업 추가
            priority_queue.put((priority, (new_product, product_name, cate_name, content, calories, sugars, protein, caffeine, fat, sodium, image_path)))


def get_all_starbucks_data(request):
    menus = Product.objects.all()

    data = [{'id': menu.id,
             'new_product': menu.new_product,
             'product_name': menu.product_name,
             'cate_name': menu.cate_name,
             'content': menu.content,
             'calories': menu.calories,
             'sugars': menu.sugars,
             'protein': menu.protein,
             'caffeine': menu.caffeine,
             'fat': menu.fat,
             'sodium': menu.sodium,
             'imageUrl': menu.imageUrl} for menu in menus]

    return JsonResponse(data, safe=False)


def get_starbucks_data(request, field_name, field_value):
    menus = Product.objects.filter(**{field_name: field_value})

    if not menus.exists():
        return JsonResponse({'error': 'Menu not found'}, status=404)

    data = serialize('json', menus)
    return JsonResponse(data, safe=False)



# 작업 스레드 함수
def worker():
    while True:
        # 우선순위 큐에서 작업 가져오기
        priority, data = priority_queue.get()

        # 이미 존재하는 상품인지 확인
        try:
            existing_product = Product.objects.get(product_name=data[1])
            print(f"Product '{existing_product.product_name}' already exists. Skipping...")
            continue  # 이미 존재하는 상품인 경우 추가하지 않고 다음 작업으로 넘어감
        except ObjectDoesNotExist:
            pass  # 해당 상품이 존재하지 않으면 계속 진행

        # 크롤링 작업 수행
        with transaction.atomic():
            Product.objects.create(
                new_product=data[0],
                product_name=data[1],
                cate_name=data[2],
                content=data[3],
                calories=data[4],
                sugars=data[5],
                protein=data[6],
                caffeine=data[7],
                fat=data[8],
                sodium=data[9],
                imageUrl=data[10]
            )

        # 작업 완료 메시지 출력
        print("Task completed successfully.")

# 응답 함수
# 응답 함수
def index(request):
    if not priority_queue.empty():  # 큐가 비어 있는지 확인하여 작업을 중복 실행하지 않도록 함
        print('Data fetching and saving process already initiated.')
        return JsonResponse({'message': 'Data fetching and saving process already initiated.'})

    print('Data fetching and saving process initiated.')
    fetch_and_save_starbucks_data()  # 데이터 가져오고 저장하는 작업 실행
    return JsonResponse({'message': 'Data fetching and saving process initiated.'})


# 스레드 생성 및 시작
fetch_thread = threading.Thread(target=fetch_and_save_starbucks_data)
fetch_thread.daemon = True
fetch_thread.start()

worker_thread = threading.Thread(target=worker)
worker_thread.daemon = True
worker_thread.start()