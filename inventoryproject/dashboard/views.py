from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Product
from .forms import ProductForm

# Create your views here.

@login_required(login_url='user-login')
def index(request):
    return render(request, 'dashboard/index.html', {})

@login_required(login_url='user-login')
def staff(request):
    return render(request, 'dashboard/staff.html', {})

@login_required(login_url='user-login')
def product(request):
    items = Product.objects.all()
    # items = Product.objects.raw('SELECT * FROM dashboard_product')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        form = ProductForm()

    context = {
        'items': items,
        'form': form,
    }
    return render(request, 'dashboard/product.html', context)

@login_required(login_url='user-login')
def order(request):
    return render(request, 'dashboard/order.html', {})