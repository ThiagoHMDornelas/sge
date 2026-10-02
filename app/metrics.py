from django.utils.formats import number_format
from django.db.models import Sum, F
from django.utils import timezone

from product.models import Product
from outflow.models import OutFlow
from category.models import Category
from brands.models import Brand


def get_sales_metrics():
    total_sales = OutFlow.objects.count()
    total_product_sold = OutFlow.objects.aggregate(
        total_product_sold=Sum('quantity')
    )['total_product_sold'] or 0

    total_sales_cost = 0
    total_sales_value = 0
    for outflows in OutFlow.objects.all():
        total_sales_cost += outflows.product.cost_price * outflows.quantity
        total_sales_value += outflows.product.selling_price * outflows.quantity

    total_sales_profit = total_sales_value - total_sales_cost

    return dict(
        total_sales=total_sales,
        total_product_sold=total_product_sold,
        total_sales_value=number_format(total_sales_value, decimal_pos=2, force_grouping=True),
        total_sales_profit=number_format(total_sales_profit, decimal_pos=2, force_grouping=True),
    )


def get_product_metrics():
    products = Product.objects.all()
    total_quantity = 0
    total_cost_price = 0
    total_selling_price = 0
    total_profit = 0
    for product in products:
        total_quantity += product.quantity
        total_cost_price += product.cost_price * product.quantity
        total_selling_price += product.selling_price * product.quantity

    total_profit = total_selling_price - total_cost_price

    return dict(
        total_quantity=total_quantity,
        total_cost_price=number_format(total_cost_price, decimal_pos=2, force_grouping=True),
        total_selling_price=number_format(total_selling_price, decimal_pos=2, force_grouping=True),
        total_profit=number_format(total_profit, decimal_pos=2, force_grouping=True)
    )


def get_daily_sales_data():
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    values = list()

    for date in dates:  # SGE - 049
        sales_total = OutFlow.objects.filter(
            created_at__date=date
        ).aggregate(
            total_sales=Sum(F('product__selling_price') * F('quantity'))
        )['total_sales'] or 0
        values.append(float(sales_total))

    return dict(
        dates=dates,
        values=values,
    )


def get_daily_sales_quantity_data():
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    quantities = list()

    for date in dates:
        sales_quantity = OutFlow.objects.filter(created_at__date=date).count()
        quantities.append(sales_quantity)

    return dict(
        dates=dates,
        values=quantities,
    )


def get_graphic_product_category_metric():
    categories = Category.objects.all()
    return {category.name: Product.objects.filter(category=category).count() for category in categories}


def get_graphic_product_brand_metric():
    brands = Brand.objects.all()
    return {brand.name: Product.objects.filter(brand=brand).count() for brand in brands}
