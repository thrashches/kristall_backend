# Generated by Django 5.0 on 2024-01-25 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_address_order_comment_order_delivery_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='retail',
            new_name='retail_office',
        ),
    ]
