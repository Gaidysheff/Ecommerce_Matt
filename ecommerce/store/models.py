from django.db import models
from django.conf import settings
from django.shortcuts import reverse


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Item(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    price = models.FloatField(verbose_name='Цена')
    discount_price = models.FloatField(
        blank=True, null=True, verbose_name='Цена со скидкой')
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=2, verbose_name='Категория')
    label = models.CharField(choices=LABEL_CHOICES,
                             max_length=1, verbose_name='Лейба')
    slug = models.SlugField(verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse("store:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Заказчик')
    ordered = models.BooleanField(default=False, verbose_name='Заказано')
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    class Meta:
        verbose_name = 'Заказ-Товар'
        verbose_name_plural = 'Заказы-Товары'

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


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

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total
