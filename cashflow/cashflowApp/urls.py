from django.urls import path
from . import views

app_name = 'cashflowApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('record/create/', views.record_create, name='record_create'),
    path('record/edit/<int:pk>/', views.record_edit, name='record_edit'),
    path('record/delete/<int:pk>/', views.record_delete, name='record_delete'),

    # Управление справочниками
    path('references/', views.reference_list, name='reference_list'),
    path('references/status/create/', views.status_create, name='status_create'),
    path('references/status/edit/<int:pk>/', views.status_edit, name='status_edit'),
    path('references/status/delete/<int:pk>/', views.status_delete, name='status_delete'),

    path('references/type/create/', views.type_create, name='type_create'),
    path('references/type/edit/<int:pk>/', views.type_edit, name='type_edit'),
    path('references/type/delete/<int:pk>/', views.type_delete, name='type_delete'),

    path('references/category/create/', views.category_create, name='category_create'),
    path('references/category/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('references/category/delete/<int:pk>/', views.category_delete, name='category_delete'),

    path('references/subcategory/create/', views.subcategory_create, name='subcategory_create'),
    path('references/subcategory/edit/<int:pk>/', views.subcategory_edit, name='subcategory_edit'),
    path('references/subcategory/delete/<int:pk>/', views.subcategory_delete, name='subcategory_delete'),
]
