from django.contrib import admin
from django.utils.html import format_html
from .models import Status, Type, Category, Subcategory, CashFlowRecord


# Базовый класс админки, для избежания повторения <record_count>
class BaseAdmin(admin.ModelAdmin):
    # Дополнительное поле, которое показывает количество записей
    def record_count(self, obj):
        count = obj.cashflowrecord_set.count()
        return format_html('<span class="badge bg-primary">{}</span>', count)

    record_count.short_description = 'Используется в записи'


# Регистрация справочников
@admin.register(Status)
class StatusAdmin(BaseAdmin):
    list_display = ['id', 'name', 'record_count']
    list_display_links = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Type)
class TypeAdmin(BaseAdmin):
    list_display = ['id', 'name', 'category_count', 'record_count']
    list_display_links = ['name']
    search_fields = ['name']
    ordering = ['name']

    # Дополнительное поле, которое показывает количество категорий
    def category_count(self, obj):
        count = obj.categories.count()
        return format_html('<span class="badge bg-info">{}</span>', count)

    category_count.short_description = 'Категория'


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ['id', 'name', 'type', 'subcategory_count', 'record_count']
    list_display_links = ['name']
    list_filter = ['type']
    search_fields = ['name', 'type__name']
    ordering = ['type', 'name']
    autocomplete_fields = ['type']

    # Дополнительное поле, которое показывает количество подкатегорий
    def subcategory_count(self, obj):
        count = obj.subcategories.count()
        return format_html('<span class="badge bg-info">{}</span>', count)

    subcategory_count.short_description = 'Подкатегория'


# Регистрация модели подкатегории
@admin.register(Subcategory)
class SubcategoryAdmin(BaseAdmin):
    list_display = ['id', 'name', 'category', 'type_display', 'record_count']
    list_display_links = ['name']
    list_filter = ['category', 'category__type']
    search_fields = ['name', 'category__name']
    ordering = ['category', 'name']
    autocomplete_fields = ['category']

    # Показываем тип через категорию
    def type_display(self, obj):
        return obj.category.type.name

    type_display_short_description = 'Тип'


# Настройка админки для записей ДДС
@admin.register(CashFlowRecord)
class CashFlowRecordAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'date',
        'status',
        'type',
        'category',
        'subcategory',
        'amount',
        'comment',
    ]
    list_display_links = ['date', 'id']
    list_filter = [
        'date',
        'status',
        'type',
        'category',
        'subcategory',
    ]
    search_fields = [
        'comment',
        'status__name',
        'type__name',
        'category__name',
        'subcategory__name',
    ]
    ordering = ['-date']
