# Generated by Django 5.0 on 2023-12-25 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.CharField(default=None, max_length=1000),
            preserve_default=False,
        ),
    ]
