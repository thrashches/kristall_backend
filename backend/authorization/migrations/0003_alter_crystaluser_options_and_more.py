# Generated by Django 5.0 on 2023-12-20 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_alter_crystaluser_auth_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crystaluser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='crystaluser',
            name='auth_type',
            field=models.CharField(choices=[('phone', 'Phone'), ('mail', 'Mail'), ('google', 'Google'), ('vk', 'VK'), ('password', 'PSW')], max_length=10, verbose_name='Тип авторизации'),
        ),
        migrations.AlterField(
            model_name='crystaluser',
            name='code',
            field=models.CharField(max_length=20, null=True, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='crystaluser',
            name='identifier',
            field=models.CharField(max_length=100, verbose_name='Идентификатор'),
        ),
    ]