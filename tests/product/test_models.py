import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from product.models import Category, Product, ProductLine

# this gives us access to database
pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        category = category_factory(name="test_category")
        assert category.__str__() == "test_category"

    def test_name_max_length(self, category_factory):
        name = 'x' * 236
        category = category_factory(name=name)
        with pytest.raises(ValidationError):
            category.full_clean()

    def test_slug_max_length(self, category_factory):
        slug = 'x' * 256
        category = category_factory(slug=slug)
        with pytest.raises(ValidationError):
            category.full_clean()

    def test_name_unique_field(self, category_factory):
        category_factory(name="test_cat")
        with pytest.raises(IntegrityError):
            category_factory(name='test_cat')

    def test_slug_unique_field(self, category_factory):
        category_factory(slug='test_slug')
        with pytest.raises(IntegrityError):
            category_factory(slug='test_slug')

    def test_is_active_true_default(self, category_factory):
        category = category_factory()
        assert category.is_active is True

    def test_parent_category_on_delete_protect(self, category_factory):
        parent = category_factory()
        category_factory(parent=parent)
        with pytest.raises(IntegrityError):
            parent.delete()

    def test_parent_field_null(self, category_factory):
        parent = category_factory()
        assert parent.parent is None

    def test_return_category_active_only_true(self, category_factory):
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.is_active().count()
        assert qs == 1

    def test_return_category_active_only_false(self, category_factory):
        category_factory(is_active=False)
        category_factory(is_active=True)
        qs = Category.objects.count()
        assert qs == 2


class TestProductModel:
    def test_str_method(self, product_factory):
        product = product_factory(name='test_product')
        assert product.__str__() == 'test_product'

    def test_fk_product_type_on_delete_protect(self, product_type_factory, product_factory):
        product = product_type_factory()
        product_factory(product_type=product)
        with pytest.raises(IntegrityError):
            product.delete()

    def test_name_max_length(self, product_factory):
        name = 'x' * 236
        product = product_factory(name=name)
        with pytest.raises(ValidationError):
            product.full_clean()

    def test_slug_max_length(self, product_factory):
        slug = 'x' * 256
        product = product_factory(slug=slug)
        with pytest.raises(ValidationError):
            product.full_clean()

    def test_pid_max_length(self, product_factory):
        pid = '0' * 11
        product = product_factory(pid=pid)
        with pytest.raises(ValidationError):
            product.full_clean()

    def test_is_digital_false_default(self, product_factory):
        product = product_factory()
        assert product.is_digital is False

    def test_fk_category_on_delete_protect(self, category_factory, product_factory):
        obj1 = category_factory()
        product_factory(category=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_return_product_active_only_true(self, product_factory):
        product_factory(is_active=True)
        product_factory(is_active=False)
        assert Product.objects.is_active().count() == 1

    def test_return_all_products(self, product_factory):
        product_factory(is_active=True)
        product_factory(is_active=False)
        assert Product.objects.count() == 2


class TestProductLineModel:

    def test_duplicate_attribute_inserts(self, product_line_factory, attribute_factory, attribute_value_factory,
                                         product_line_attribute_value_factory):
        attribute = attribute_factory(name='shoe-color')
        attribute_value = attribute_value_factory(attribute=attribute, attribute_value='red')
        attribute_value2 = attribute_value_factory(attribute=attribute, attribute_value='blue')
        product_line = product_line_factory()
        product_line_attribute_value_factory(attribute_value=attribute_value, product_line=product_line)
        with pytest.raises(ValidationError):
            product_line_attribute_value_factory(attribute_value=attribute_value2, product_line=product_line)

    def test_str_method(self, product_line_factory):
        obj = product_line_factory(sku='12345')
        assert obj.__str__() == '12345'

    def test_fk_product_type_on_delete_protect(self, product_type_factory, product_line_factory):
        product_type = product_type_factory()
        product_line_factory(product_type=product_type)
        with pytest.raises(IntegrityError):
            product_type.delete()

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        product = product_factory()
        product_line_factory(order=1, product=product)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=product).clean()

    def test_field_decimal_places(self, product_line_factory):
        price = 1.001
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_field_price_max_digits(self, product_line_factory):
        price = 1000.00
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_sku_max_length(self, product_line_factory):
        sku = '0123456789123'
        with pytest.raises(ValidationError):
            product_line_factory(sku=sku)

    def test_is_active_false_default(self, product_line_factory):
        product_line = product_line_factory()
        assert product_line.is_active is False

    def test_fk_product_on_delete_protect(self, product_factory, product_line_factory):
        product = product_factory()
        product_line_factory(product=product)
        with pytest.raises(IntegrityError):
            product.delete()

    def test_return_product_line_active_only_true(self, product_line_factory):
        product_line = product_line_factory(is_active=True)
        product_line2 = product_line_factory(is_active=False)
        assert ProductLine.objects.is_active().count() == 1

    def test_return_all_product_lines(self, product_line_factory):
        product_line = product_line_factory(is_active=True)
        product_line2 = product_line_factory(is_active=False)
        assert Product.objects.count() == 2


class TestProductImageModel:
    def test_str_method(self, product_image_factory, product_line_factory):
        product_line = product_line_factory(sku='12345')
        product_image = product_image_factory(url='test.jpg', product_line=product_line)
        assert product_image.__str__() == '12345_img'

    def test_alternative_text_max_length(self, product_image_factory):
        alternative_text = 'x' * 236
        with pytest.raises(ValidationError):
            product_image_factory(alternative_text=alternative_text)

    def test_duplicate_order_values(self, product_image_factory, product_line_factory):
        product_line = product_line_factory()
        product_image_factory(order=1, product_line=product_line)
        with pytest.raises(ValidationError):
            product_image_factory(order=1, product_line=product_line).clean()


class TestProductTypeModel:
    def test_str_method(self, product_type_factory):
        obj = product_type_factory.create(name='test_type')
        assert obj.__str__() == 'test_type'

    def test_name_field_max_length(self, product_type_factory):
        name = 'x' * 101
        product_type = product_type_factory(name=name)
        with pytest.raises(ValidationError):
            product_type.full_clean()


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        attribute = attribute_factory(name='test_attribute')
        assert attribute.__str__() == 'test_attribute'

    def test_name_field_max_length(self, attribute_factory):
        name = 'x' * 101
        attribute = attribute_factory(name=name)
        with pytest.raises(ValidationError):
            attribute.full_clean()


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory, attribute_factory):
        obj_a = attribute_factory(name='test_attribute')
        obj_b = attribute_value_factory(attribute_value='test_value', attribute=obj_a)
        assert obj_b.__str__() == 'test_attribute-test_value'

    def test_value_field_max_length(self, attribute_value_factory):
        attribute_value = 'x' * 101
        obj = attribute_value_factory(attribute_value=attribute_value)
        with pytest.raises(ValidationError):
            obj.full_clean()
