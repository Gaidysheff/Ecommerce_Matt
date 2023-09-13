from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField


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

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
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
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата начала заказа')
    ordered_date = models.DateTimeField(verbose_name='Дата заказа')
    ordered = models.BooleanField(default=False, verbose_name='Заказано')
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Адрес доставки')
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Адрес проживания')
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Оплата')
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Купон')
    being_delivered = models.BooleanField(
        default=False, verbose_name='Доставляется')
    received = models.BooleanField(default=False, verbose_name='Получено')
    refund_requested = models.BooleanField(
        default=False, verbose_name='Запрос на возмещение')
    refund_granted = models.BooleanField(
        default=False, verbose_name='Возмещено')

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    # def display_orders(self):
    #     return ', '.join([x.item for x in self.items.all()])

    # display_orders.short_description = 'Товары'

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Заказчик')
    street_address = models.CharField(max_length=100, verbose_name='Улица')
    apartment_address = models.CharField(
        max_length=100, verbose_name='дом, квартира')
    country = CountryField(multiple=False, verbose_name='Страна')
    zip = models.CharField(max_length=100, verbose_name='Индекс')
    address_type = models.CharField(
        max_length=1, choices=ADDRESS_CHOICES, verbose_name='Тип адреса')
    default = models.BooleanField(default=False, verbose_name='По умолчанию')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50, verbose_name='id карты')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             blank=True, null=True, verbose_name='Покупатель')
    amount = models.FloatField(verbose_name='Сумма')
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата/Время')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = 'Возмещение'
        verbose_name_plural = 'Возмещения'
