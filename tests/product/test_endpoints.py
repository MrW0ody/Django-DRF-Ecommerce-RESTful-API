import pytest
import json

# this gives us access to database
pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    endpoint = '/api/category/'

    def test_category_get(self, category_factory, api_client):
        category_factory.create_batch(4)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4


class TestProductEndpoints:
    endpoint = '/api/product/'

    def test_return_product_by_category_slug(self, category_factory, product_factory, api_client):
        category = category_factory(slug='test_slug')
        product_factory(category=category)
        response = api_client().get(f'{self.endpoint}category/{category.slug}/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1
