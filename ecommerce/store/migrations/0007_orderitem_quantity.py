# Generated by Django 4.2.4 on 2023-09-01 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='Количество'),
        ),
    ]
