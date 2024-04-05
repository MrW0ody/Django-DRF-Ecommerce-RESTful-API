import pytest
from django.core.exceptions import ValidationError

# this gives us access to database
pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        category = category_factory(name="test_category")
        assert category.__str__() == "test_category"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        brand = brand_factory(name='test_brand')
        assert brand.__str__() == 'test_brand'


class TestProductModel:
    def test_str_method(self, product_factory):
        product = product_factory(name='test_product')
        assert product.__str__() == 'test_product'


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        product_line = product_line_factory(sku='12345')
        assert product_line.__str__() == '12345'

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        product = product_factory()
        product_line_factory(order=1, product=product)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=product).clean()


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        product_image = product_image_factory(url='test.jpg')
        assert product_image.__str__() == 'test.jpg'
