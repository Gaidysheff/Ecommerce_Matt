# Generated by Django 4.2.4 on 2023-09-01 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_item_description_alter_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='q', upload_to=''),
            preserve_default=False,
        ),
    ]
