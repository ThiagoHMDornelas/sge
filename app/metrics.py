from django.db.models import Count, F, Sum
from django.db.models.functions import Lower, TruncDate
from django.utils import timezone
from django.utils.formats import number_format

from brands.models import Brand
from category.models import Category
from outflow.models import OutFlow
from product.models import Product


def get_sales_metrics():
    totals = OutFlow.objects.aggregate(
        total_sales=Count('id'),
        total_product_sold=Sum('quantity'),
        total_sales_value=Sum(F('product__selling_price') * F('quantity')),
        total_sales_cost=Sum(F('product__cost_price') * F('quantity')),
    )
    value = totals['total_sales_value'] or 0
    cost = totals['total_sales_cost'] or 0

    return dict(
        total_sales=totals['total_sales'] or 0,
        total_product_sold=totals['total_product_sold'] or 0,
        total_sales_value=number_format(value, decimal_pos=2, force_grouping=True),
        total_sales_profit=number_format(value - cost, decimal_pos=2, force_grouping=True),
    )


def get_product_metrics():
    totals = Product.objects.aggregate(
        total_quantity=Sum('quantity'),
        total_cost_price=Sum(F('cost_price') * F('quantity')),
        total_selling_price=Sum(F('selling_price') * F('quantity')),
    )
    cost = totals['total_cost_price'] or 0
    selling = totals['total_selling_price'] or 0

    return dict(
        total_quantity=totals['total_quantity'] or 0,
        total_cost_price=number_format(cost, decimal_pos=2, force_grouping=True),
        total_selling_price=number_format(selling, decimal_pos=2, force_grouping=True),
        total_profit=number_format(selling - cost, decimal_pos=2, force_grouping=True),
    )


def _daily_series(expression):
    today = timezone.now().date()
    start = today - timezone.timedelta(days=6)

    rows = (
        OutFlow.objects
        .filter(created_at__date__gte=start)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=expression)
    )
    totals = {row['day']: row['total'] for row in rows}

    dates = [start + timezone.timedelta(days=i) for i in range(7)]
    return dates, totals


def get_daily_sales_data():
    dates, totals = _daily_series(Sum(F('product__selling_price') * F('quantity')))
    return dict(
        dates=[str(date) for date in dates],
        values=[float(totals.get(date) or 0) for date in dates],
    )


def get_daily_sales_quantity_data():
    dates, totals = _daily_series(Count('id'))
    return dict(
        dates=[str(date) for date in dates],
        values=[totals.get(date) or 0 for date in dates],
    )


def get_graphic_product_category_metric():
    rows = (
        Category.objects
        .annotate(total=Count('product_category'))
        .order_by(Lower('name'))
        .values_list('name', 'total')
    )
    return dict(rows)


def get_graphic_product_brand_metric():
    rows = (
        Brand.objects
        .annotate(total=Count('product_brand'))
        .order_by(Lower('name'))
        .values_list('name', 'total')
    )
    return dict(rows)
