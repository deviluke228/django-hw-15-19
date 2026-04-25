from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models


def validate_even(val):
    if val % 2 != 0:
        raise ValidationError(
            'Число %(value)s нечётное',
            code='odd',
            params={'value': val}
        )


# -----------------------
# RUBRIC
# -----------------------
class Rubric(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='Название',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ('name',)


# -----------------------
# BBOARD
# -----------------------
class Bb(models.Model):
    KINDS = (
        ('Купля-продажа', (
            ('b', 'Куплю'),
            ('s', 'Продам'),
        )),
        ('Обмен', (
            ('c', 'Обменяю'),
        )),
    )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s',
        verbose_name='Тип объявления',
    )

    title = models.CharField(
        max_length=50,
        verbose_name='Товар',
        validators=[
            validators.RegexValidator(regex='^.{4,}$'),
        ],
        error_messages={'invalid': 'Введите не менее 4 символов'}
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )

    # ✔ BBCode поле (ИСПРАВЛЕНО)
    content_bb = models.TextField(
        null=True,
        blank=True,
        verbose_name="BBCode описание"
    )

    price = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Цена',
        validators=[validate_even],
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано',
    )

    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    def __str__(self):
        return f'Объявление: {self.title}'

    def title_and_price(self):
        return f'{self.title} ({self.price})' if self.price else self.title

    title_and_price.short_description = 'Название и цена'

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание товара')

        if self.price and self.price < 0:
            errors['price'] = ValidationError('Цена не может быть отрицательной')

        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published']


# -----------------------
# ICE CREAM MANAGER (ВАЖНО: ВЫШЕ МОДЕЛИ)
# -----------------------
class IceCreamManager(models.Manager):
    def available(self):
        return self.filter(is_available=True)


# -----------------------
# ICE CREAM
# -----------------------
class IceCream(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    flavor = models.CharField(max_length=50, verbose_name="Вкус")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")

    objects = IceCreamManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мороженое"
        verbose_name_plural = "Мороженое"


# -----------------------
# TOPPING
# -----------------------
class Topping(models.Model):
    name = models.CharField(max_length=50, verbose_name="Топпинг")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Топпинг"
        verbose_name_plural = "Топпинги"


# -----------------------
# MANY TO MANY SET
# -----------------------
class IceCreamSet(models.Model):
    name = models.CharField(max_length=100, verbose_name="Набор")

    icecreams = models.ManyToManyField(IceCream)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return self.name


# -----------------------
# ABSTRACT + INHERITANCE
# -----------------------
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Food(Product):
    expiration_date = models.DateField()


class PremiumIceCream(Food):
    flavor = models.CharField(max_length=50)
    is_organic = models.BooleanField(default=False)


# -----------------------
# CONTACT FORM SAVE MODEL
# -----------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name