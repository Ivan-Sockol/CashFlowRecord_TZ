from django import forms
from django.core.exceptions import ValidationError
from .models import CashFlowRecord, Status, Type, Category, Subcategory
from datetime import date


# Создаем форму на основе модели - CashFlowRecord
class CashFlowRecordForm(forms.ModelForm):
    class Meta:
        model = CashFlowRecord
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Установка даты по умолчанию
        if not self.instance.pk:
            self.fields['date'].initial = date.today()

        # показываем все категории и подкатегори
        # Фильтрация будет только на сервере при валидации
        self.fields['category'].queryset = Category.objects.all()
        self.fields['subcategory'].queryset = Subcategory.objects.all()

        # Делаем поля обязательными
        self.fields['type'].required = True
        self.fields['category'].required = True
        self.fields['subcategory'].required = True
        self.fields['amount'].required = True

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        type_obj = cleaned_data.get('type')

        # валидация на сервере
        if category and subcategory:
            if subcategory.category_id != category.id:
                raise ValidationError({
                    'subcategory': 'Выбранная подкатегория не относится к указанной категории'
                })

        if type_obj and category:
            if category.type_id != type_obj.id:
                raise ValidationError({
                    'category': 'Выбранная категория не относится к указанному типу'
                })

        amount = cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise ValidationError({
                'amount': 'Сумма должна быть больше нуля'
            })

        return cleaned_data


# Формы для справочников
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'})
        }


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
