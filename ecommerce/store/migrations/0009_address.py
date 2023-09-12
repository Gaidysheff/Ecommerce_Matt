# Generated by Django 4.2.4 on 2023-09-11 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0008_alter_item_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=100, verbose_name='Улица')),
                ('apartment_address', models.CharField(max_length=100, verbose_name='дом, квартира')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Страна')),
                ('zip', models.CharField(max_length=100, verbose_name='Индекс')),
                ('address_type', models.CharField(choices=[('B', 'Billing'), ('S', 'Shipping')], max_length=1, verbose_name='Тип адреса')),
                ('default', models.BooleanField(default=False, verbose_name='По умолчанию')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
            },
        ),
    ]