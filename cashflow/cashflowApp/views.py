from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CashFlowRecord, Status, Type, Category, Subcategory
from .forms import CashFlowRecordForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm
from datetime import datetime


def index(request):
    records = CashFlowRecord.objects.all()

    # Фильтрация
    date_from = request.GET.get('date_form')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    if date_from:
        try:
            records = records.filter(date__gte=datetime.strptime(date_from, '%Y-%m-%d'))
        except ValueError:
            pass
    if date_to:
        try:
            records = records.filter(date__lte=datetime.strptime(date_to, '%Y-%m-%d'))
        except ValueError:
            pass
    if status_id:
        records = records.filter(status_id=status_id)
    if type_id:
        records = records.filter(type_id=type_id)
    if category_id:
        records = records.filter(category_id=category_id)
    if subcategory_id:
        records = records.filter(category_id=category_id)

    context = {
        'records': records,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'filters': {
            'date_from': date_from,
            'date_to': date_to,
            'status': status_id,
            'type': type_id,
            'category': category_id,
            'subcategory': subcategory_id
        }
    }
    return render(request, 'index.html', context)


def record_create(request):
    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно создана')
            return redirect('cashflowApp:index')
    else:
        form = CashFlowRecordForm()
    context = {
        'form': form,
        'title': 'Создание записи',
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    }
    return render(request, 'record_form.html', context)


def record_edit(request, pk):
    record = get_object_or_404(CashFlowRecord, pk=pk)
    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена')
            return redirect('cashflowApp:index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = CashFlowRecordForm(initial=record)
    context = {
        'form': form,
        'title': 'Редактирование записи',
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'record': record,
    }
    return render(request, 'record_form.html', context)


def record_delete(request, pk):
    record = get_object_or_404(CashFlowRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Запись успешно удалена')
        return redirect('cashflowApp:index')
    return render(request, 'record_confirm_delete.html', {'record': record})


# Управление справочниками
def reference_list(request):
    context = {
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all()
    }
    return render(request, 'reference_list.html', context)


# Статусы
def status_create(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно добавлен')
            return redirect('cashflowApp:reference_list')
    else:
        form = StatusForm()
    return render(request, 'reference_form.html',
                  {'form': form,
                   'title': 'Добавление статуса',
                   'back_url': 'reference_list'})


def status_edit(request, pk):
    obj = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно обновлен')
            return redirect('cashflowApp:reference_list')
    else:
        form = StatusForm(instance=obj)
    return render(request, 'reference_form.html',
                  {'form': form,
                   'title': 'Редактирование статуса',
                   'back_url': 'reference_list'})


def status_delete(request, pk):
    obj = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, 'Статус успешно удален')
        except:
            messages.error(request, 'Невозможно удалить статус так ак он используется в записях')
        return redirect('cashflowApp:reference_list')
    return render(request, 'reference_confirm_delete.html',
                  {'obj': obj,
                   'title': 'Удаление статуса',
                   'back_url': 'reference_list'})


# Типы
def type_create(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип успешно создан')
            return redirect('cashflowApp:reference_list')
    else:
        form = TypeForm()
    return render(request, 'reference_form.html',
                  {'form': form,
                   'title': 'Добавление типа',
                   'back_url': 'reference_list'})


def type_edit(request, pk):
    obj = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        form = TypeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип успешно изменен')
            return redirect('cashflowApp:reference_list')
    else:
        form = TypeForm(instance=obj)
    return render(request,
                  'reference_form.html',
                  {'form': form,
                   'title': 'Редактирование типа',
                   'back_url': 'reference_list'})


def type_delete(request, pk):
    obj = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, 'Тип успешно удалён')
        except:
            messages.error(request, 'Невозможно удалить тип, так как он используется в записях')
        return redirect('cashflowApp:reference_list')
    return render(request, 'reference_confirm_delete.html',
                  {'obj': obj,
                   'title': 'Удаление типа',
                   'back_url': 'reference_list'})


# Категория
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно добавлена')
            return redirect('cashflowApp:reference_list')
    else:
        form = CategoryForm()
    return render(request, 'reference_form.html',
                  {'form': form, 'title': 'Добавление категории',
                   'back_url': 'reference_list'})


def category_edit(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно обновлена')
            return redirect('cashflowApp:reference_list')
    else:
        form = CategoryForm(instance=obj)
    return render(request, 'reference_form.html',
                  {'form': form, 'title': 'Редактирование категории',
                   'back_url': 'reference_list'})


def category_delete(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, 'Категория успешно удалена')
        except:
            messages.error(request, 'Невозможно удалить категорию, так как она используется в записях')
        return redirect('cashflowApp:reference_list')
    return render(request, 'reference_confirm_delete.html',
                  {'obj': obj, 'title': 'Удаление категории',
                   'back_url': 'reference_list'})


# Подкатегории
def subcategory_create(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подкатегория успешно добавлена')
            return redirect('cashflowApp:reference_list')
    else:
        form = SubcategoryForm()
    return render(request, 'reference_form.html',
                  {'form': form, 'title': 'Добавление подкатегории',
                   'back_url': 'reference_list'})


def subcategory_edit(request, pk):
    obj = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подкатегория успешно обновлена')
            return redirect('cashflowApp:reference_list')
    else:
        form = SubcategoryForm(instance=obj)
    return render(request, 'reference_form.html',
                  {'form': form, 'title': 'Редактирование подкатегории',
                   'back_url': 'reference_list'})


def subcategory_delete(request, pk):
    obj = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, 'Подкатегория успешно удалена')
        except:
            messages.error(request, 'Невозможно удалить подкатегорию, так как она используется в записи')
        return redirect('cashflowApp:reference_list')
    return render(request, 'reference_confirm_delete.html',
                  {'obj': obj, 'title': 'Удаление подкатегории',
                   'back_url': 'reference_list'})
