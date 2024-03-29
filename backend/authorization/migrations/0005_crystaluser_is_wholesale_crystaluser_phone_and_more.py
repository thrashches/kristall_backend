# Generated by Django 5.0 on 2024-01-26 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0004_alter_crystaluser_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='crystaluser',
            name='is_wholesale',
            field=models.BooleanField(default=True, verbose_name='Оптовик'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crystaluser',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='crystaluser',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]
