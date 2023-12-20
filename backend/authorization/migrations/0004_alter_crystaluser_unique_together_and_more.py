# Generated by Django 5.0 on 2023-12-20 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('authorization', '0003_alter_crystaluser_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='crystaluser',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='crystaluser',
            name='auth_type',
            field=models.CharField(choices=[('phone', 'По телефону'), ('mail', 'По почте'), ('google', 'Google'), ('vk', 'VK'), ('password', 'По паролю')], default='password', max_length=10, verbose_name='Тип авторизации'),
        ),
        migrations.AlterField(
            model_name='crystaluser',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Код'),
        ),
        migrations.AddConstraint(
            model_name='crystaluser',
            constraint=models.UniqueConstraint(fields=('auth_type', 'identifier'), name='unique_auth_type_identifier'),
        ),
    ]
