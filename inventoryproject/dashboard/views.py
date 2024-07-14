from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

import csv
from import_export.formats.base_formats import XLSX

from .models import Product, Order
from .forms import ProductForm, OrderForm
from .resources import ProductResource

# Create your views here.

@login_required(login_url='user-login')
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    product_count = products.count()
    orders_count = orders.count()
    workers_count = User.objects.all().count()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('index')
    else:
        form = OrderForm()
    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'product_count': product_count,
        'orders_count': orders_count,
        'workers_count': workers_count,
    }
    return render(request, 'dashboard/index.html', context)

@login_required(login_url='user-login')
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    context = {
        'workers': workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required(login_url='user-login')
def staff_detail(request, pk):
    workers = User.objects.get(id=pk)
    context = {
        'workers': workers,
    }
    return render(request, 'dashboard/staff_detail.html', context)

@login_required(login_url='user-login')
def product(request):
    items = Product.objects.all()
    product_count = items.count()
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()

    # Initialize the form variable
    form = ProductForm()

    if request.method == 'POST':
        if 'upload' in request.POST:
            product_resource = ProductResource()
            new_products = request.FILES['file']
            dataset = XLSX().create_dataset(new_products.read())
            result = product_resource.import_data(dataset, dry_run=True)  # Dry run for validation

            if not result.has_errors():
                product_resource.import_data(dataset, dry_run=False)  # Actually import now
                messages.success(request, 'Products imported successfully')
            else:
                messages.error(request, 'There was an error importing the products')

        elif 'export' in request.POST:
            product_resource = ProductResource()
            dataset = product_resource.export()
            xlsx_format = XLSX()
            xlsx_data = xlsx_format.export_data(dataset)
            response = HttpResponse(xlsx_data, content_type=xlsx_format.get_content_type())
            response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
            return response

        else:
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
                product_name = form.cleaned_data.get('name')
                messages.success(request, f'{product_name} has been added')
                return redirect('product')

    context = {
        'items': items,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/product.html', context)


def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('product')
    return render(request, 'dashboard/product_delete.html')


def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form
    }
    return render(request, 'dashboard/product_update.html', context)


@login_required(login_url='user-login')
def order(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count()
    product_count = Product.objects.all().count()
    context = {
        'orders': orders,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/order.html', context)