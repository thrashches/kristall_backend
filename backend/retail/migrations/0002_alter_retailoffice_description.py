# Generated by Django 5.0 on 2024-01-19 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retailoffice',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
