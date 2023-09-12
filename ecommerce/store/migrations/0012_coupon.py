# Generated by Django 4.2.4 on 2023-09-12 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_payment_order_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('amount', models.FloatField()),
            ],
            options={
                'verbose_name': 'Купон',
                'verbose_name_plural': 'Купоны',
            },
        ),
    ]