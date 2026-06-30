from django.core.validators import MinValueValidator
from django.db import models


# Модель записи ДДС решил реализовать через "справочники", чтобы обеспечить необходимую гибкость.

class Status(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Статус'  # Название для админки
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    type = models.ForeignKey('Type',
                             on_delete=models.CASCADE,
                             related_name='categories',
                             verbose_name='Тип')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        # Комбинация name и type должна быть уникальной. Нельзя создать две категории "Маркетинг" для одного поля
        unique_together = ('name', 'type')

    def __str__(self):
        return f'{self.name} - {self.type.name}'


class Subcategory(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 related_name='subcategories',
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        # В одной категории не может быть двух подкатегорий с одинаковым названием
        unique_together = ('name', 'category')

    def __str__(self):
        return f'{self.name} ({self.category.name})'


class CashFlowRecord(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date = models.DateField(verbose_name='Дата записи')
    status = models.ForeignKey('Status',
                               on_delete=models.PROTECT,  # Нельзя удалить статус, если на него есть ссылки в записях
                               verbose_name='Статус')
    type = models.ForeignKey('Type',
                             on_delete=models.PROTECT,
                             verbose_name='Тип')
    category = models.ForeignKey('Category',
                                 on_delete=models.PROTECT,
                                 verbose_name='Категория')
    subcategory = models.ForeignKey('Subcategory',
                                    on_delete=models.PROTECT,
                                    verbose_name='Подкатегория')
    amount = models.DecimalField(max_digits=12,
                                 decimal_places=2,
                                 # Валидаторы для суммы:
                                 # Сумма не может быть меньше 0.01
                                 # Нельзя ввести отрицательную сумму
                                 # Нельзя ввести 0
                                 validators=[MinValueValidator(0.01)],
                                 verbose_name='Сумма')
    comment = models.TextField(blank=True, verbose_name='Комментарий')  # Поле не обязательно к заполнению (blank=True)

    class Meta:
        verbose_name = 'Запись ДДС'
        verbose_name_plural = 'Записи ДДС'
        ordering = ['-date', '-created']  # Сортируем записи по дате (сначала новые)

    def __str__(self):
        return f'{self.date} - {self.status} - {self.amount} руб.'
