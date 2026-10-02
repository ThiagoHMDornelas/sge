from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app import metrics
from brands.models import Brand
from category.models import Category
from outflow.models import OutFlow
from product.models import Product


class MetricsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Eletrônicos')
        self.brand = Brand.objects.create(name='Sony')
        self.product = Product.objects.create(
            name='Fone', category=self.category, brand=self.brand,
            cost_price=100, selling_price=150, quantity=10,
        )


class SalesMetricsTest(MetricsTestCase):
    def test_empty(self):
        result = metrics.get_sales_metrics()
        self.assertEqual(result['total_sales'], 0)
        self.assertEqual(result['total_product_sold'], 0)
        self.assertEqual(result['total_sales_value'], '0,00')
        self.assertEqual(result['total_sales_profit'], '0,00')

    def test_with_outflows(self):
        OutFlow.objects.create(product=self.product, quantity=2)
        OutFlow.objects.create(product=self.product, quantity=3)

        result = metrics.get_sales_metrics()

        self.assertEqual(result['total_sales'], 2)
        self.assertEqual(result['total_product_sold'], 5)
        self.assertEqual(result['total_sales_value'], '750,00')
        self.assertEqual(result['total_sales_profit'], '250,00')


class ProductMetricsTest(MetricsTestCase):
    def test_product_metrics(self):
        result = metrics.get_product_metrics()

        self.assertEqual(result['total_quantity'], 10)
        self.assertEqual(result['total_cost_price'], '1.000,00')
        self.assertEqual(result['total_selling_price'], '1.500,00')
        self.assertEqual(result['total_profit'], '500,00')

    def test_empty(self):
        self.product.delete()
        result = metrics.get_product_metrics()

        self.assertEqual(result['total_quantity'], 0)
        self.assertEqual(result['total_profit'], '0,00')


class DailySalesTest(MetricsTestCase):
    def test_series_has_seven_days(self):
        result = metrics.get_daily_sales_data()
        self.assertEqual(len(result['dates']), 7)
        self.assertEqual(len(result['values']), 7)

    def test_today_sale_appears_on_last_point(self):
        OutFlow.objects.create(product=self.product, quantity=2)

        result = metrics.get_daily_sales_data()

        self.assertEqual(result['values'][-1], 300.0)
        self.assertEqual(result['values'][:-1], [0.0] * 6)

    def test_daily_quantity_counts_records(self):
        OutFlow.objects.create(product=self.product, quantity=2)
        OutFlow.objects.create(product=self.product, quantity=1)

        result = metrics.get_daily_sales_quantity_data()

        self.assertEqual(result['values'][-1], 2)


class GraphicMetricsTest(MetricsTestCase):
    def test_category_counts_include_zero(self):
        empty = Category.objects.create(name='Vazia')

        result = metrics.get_graphic_product_category_metric()

        self.assertEqual(result['Eletrônicos'], 1)
        self.assertEqual(result[empty.name], 0)

    def test_brand_counts_include_zero(self):
        empty = Brand.objects.create(name='Vazia')

        result = metrics.get_graphic_product_brand_metric()

        self.assertEqual(result['Sony'], 1)
        self.assertEqual(result[empty.name], 0)


class MetricsQueryCountTest(MetricsTestCase):
    def test_all_metrics_run_in_six_queries(self):
        OutFlow.objects.create(product=self.product, quantity=1)

        with self.assertNumQueries(6):
            metrics.get_sales_metrics()
            metrics.get_product_metrics()
            metrics.get_daily_sales_data()
            metrics.get_daily_sales_quantity_data()
            metrics.get_graphic_product_category_metric()
            metrics.get_graphic_product_brand_metric()


class HomeViewTest(MetricsTestCase):
    def test_requires_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_renders_dashboard_for_logged_user(self):
        User.objects.create_superuser(username='admin', password='senha123')
        self.client.login(username='admin', password='senha123')

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)


class ApiDocsTest(TestCase):
    def test_schema_is_served(self):
        response = self.client.get(reverse('schema'))
        self.assertEqual(response.status_code, 200)

    def test_swagger_ui_is_served(self):
        response = self.client.get(reverse('swagger-ui'))
        self.assertEqual(response.status_code, 200)
