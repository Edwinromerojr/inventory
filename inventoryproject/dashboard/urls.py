from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('staff/', views.staff, name='staff'),
    path('product/', views.product, name='product'),
    path('order/', views.order, name='order'),
]
