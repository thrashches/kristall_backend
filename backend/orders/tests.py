from decimal import Decimal

from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from authorization.models import CrystalUser
from goods.models import Category, Product, ProductImage
from orders.models import Order, WORK




def kill_image(data):
    """гадкий uuid каждый раз новый генерируется в названии image"""
    items = data.get('items')
    for item in items:
        product = item.get('product')
        image = product.get('image')
        product['image'] = len(image)
    return items


class ProductTestCase(TestCase):
    def setUp(self):
        # Создаем категории
        Category.objects.create(name='Вафельки', slug='vafli')
        Category.objects.create(name='Пироженки', slug='pirogenki')

        # Создаем продукты
        products = [
            {'title': 'Вафля с шоколадом', 'category': 'Вафельки', 'price': 50.0},
            {'title': 'Вафля с кремом', 'category': 'Вафельки', 'price': 45.0},
            {'title': 'Шоколадное пирожное', 'category': 'Пироженки', 'price': 60.0},
            {'title': 'Кремовое пирожное', 'category': 'Пироженки', 'price': 55.0},
            {'title': 'Фруктовое пирожное', 'category': 'Пироженки', 'price': 65.0},
            {'title': 'Классическое пирожное', 'category': 'Пироженки', 'price': 50.0}
        ]

        for product in products:
            category = Category.objects.get(name=product['category'])
            Product.objects.create(
                title=product['title'],
                category=category,
                price=product['price'],
                description='Описание для ' + product['title'],
                weight=1.00,
                energy=100.00
            )

        for product in Product.objects.all():
            image = SimpleUploadedFile(product.title + ".jpg", b"file_content", content_type="image/jpeg")
            ProductImage.objects.create(product=product, image_file=image)
        self.client = APIClient()
        self.user = CrystalUser.objects.create_user(username='testuser', password='12345ong!@')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_orders_(self):
        """create order1  get list of orders get order by id"""
        url = reverse('orders-list')
        data = {"items": [
            {"product": 1,
             "quantity": 2}
        ]
        }

        data2 = {"items": [
            {"product": 2,
             "quantity": 10}
        ]
        }


        result = {'items':
            [
                {'product': {'id': 1,
                             'name': 'Вафля с шоколадом',
                             'price': Decimal('50.00'),
                             'image': '/media/product_images/eddbbd16-928f-4c58-89ad-827e41199404.jpg'
                             },
                 'quantity': 2}],
            'id': 1,
            'number': None,
            'price': Decimal('100.00'),
            'status': 'in_basket'
        }
        expected_data = kill_image(result)
        # создать ордер
        response = self.client.post(url, data=data, format='json')

        got_data = kill_image(response.data)

        print('[CREATE ORDER]')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, got_data)
        #ордер в статус в работе
        order = Order.objects.last()
        order.status = WORK
        order.save()
        # получить список заказов
        print('[ORDER LIST]')
        response = self.client.get(url)
        got_data = kill_image(response.data.get('results')[0])
        self.assertEqual(expected_data, got_data)
        # получить заказ по айди
        print('[GET ORDER BY ID]')
        response = self.client.get(f"{url}1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        got_data = response.data
        got_data = kill_image(got_data)
        self.assertEqual(expected_data, got_data)
        response = self.client.put(f"{url}/cart/",data=data2,format='json')
        print(response)
        self.assertEqual(response.status_code,status.HTTP_200_OK)













