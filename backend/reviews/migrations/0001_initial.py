# Generated by Django 5.0 on 2024-02-05 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок отзыва(общее впечатление)')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('published', models.BooleanField(default=False, verbose_name='Отображать на сайте')),
                ('text', models.TextField(max_length=1000, verbose_name='Текст отзыва')),
                ('rating', models.PositiveSmallIntegerField(verbose_name='Оценка')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-id'],
            },
        ),
    ]
