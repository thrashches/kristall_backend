# Generated by Django 5.0 on 2024-01-26 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0008_alter_crystaluser_email'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='crystaluser',
            name='unique_auth_type_email',
        ),
        migrations.AlterField(
            model_name='crystaluser',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]
