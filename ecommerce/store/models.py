from django.db import models
from django.conf import settings


class Item(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    price = models.FloatField(verbose_name='Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Заказчик')
    ordered = models.BooleanField(default=False, verbose_name='Заказано')
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, verbose_name='Товар')

    # def __str__(self):
    #     return f"{self.quantity} of {self.item.title}"

    class Meta:
        verbose_name = 'Заказ-Товар'
        verbose_name_plural = 'Заказы-Товары'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Заказчик')
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата начала заказа')
    ordered_date = models.DateTimeField(verbose_name='Дата заказа')
    ordered = models.BooleanField(default=False, verbose_name='Заказано')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def display_orders(self):
        return ', '.join([x.item for x in self.items.all()])

    display_orders.short_description = 'Товары'
