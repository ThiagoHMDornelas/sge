from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.template import loader
import json
from django.contrib.auth.decorators import login_required

from . import metrics


def custom_404(request, exception=None):
    return HttpResponseNotFound(loader.get_template('404.html').render({}, request))


@login_required(login_url='login')
def home(request):
    product_metrics = metrics.get_product_metrics()
    sales_metrics = metrics.get_sales_metrics()
    daily_sales_data = metrics.get_daily_sales_data()
    daily_sales_quantity_data = metrics.get_daily_sales_quantity_data()
    product_count_by_category = metrics.get_graphic_product_category_metric()
    product_count_by_brand = metrics.get_graphic_product_brand_metric()

    context = {
        'product_metrics': product_metrics,
        'sales_metrics': sales_metrics,
        'daily_sales_data': json.dumps(daily_sales_data),  # transforma dicionario python em json para o HTML ententer
        'daily_sales_quantity_data': json.dumps(daily_sales_quantity_data),
        'product_count_by_category': json.dumps(product_count_by_category),
        'product_count_by_brand': json.dumps(product_count_by_brand),
    }
    return render(request, 'home.html', context)
