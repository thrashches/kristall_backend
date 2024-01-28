# Generated by Django 5.0 on 2024-01-27 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0009_remove_crystaluser_unique_auth_type_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='crystaluser',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AddField(
            model_name='crystaluser',
            name='company',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Компания'),
        ),
    ]
