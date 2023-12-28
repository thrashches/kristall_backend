from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APIRequestFactory
from authorization.models import CrystalUser
from goods.models import Category, Product, ProductImage

"""Чето тухло как вьюсет тестировать. не через постман же."""

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
        self.user = CrystalUser.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_product_count(self):
        self.assertEqual(Product.objects.count(), 6)
    def test_category_count(self):
        self.assertEqual(Category.objects.count(), 2)
    def test_product_images_count(self):
        self.assertEqual(ProductImage.objects.count(), 6)
    def test_orders_case(self):
        url = reverse('orders-list')
        data = {"items":[
            {"product":1,
             "quantity":2},
            {'product':2,
             'quantity':2}
        ]
                }

        factory = APIRequestFactory()
        request = factory.post('/orders/', {'title': 'new idea'})


        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data ,5)
