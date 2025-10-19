from django.test import TestCase
from django.urls import reverse
from .models import Item

class ItemModelTest(TestCase):

    def setUp(self):
        self.item = Item.objects.create(name="Apple", quantity=5)

    def test_str_method(self):
        self.assertEqual(str(self.item), "Apple")

    def test_is_in_stock_true(self):
        self.assertTrue(self.item.is_in_stock())

    def test_is_in_stock_false(self):
        self.item.quantity = 0
        self.assertFalse(self.item.is_in_stock())

class IndexViewTest(TestCase):

    def setUp(self):
        Item.objects.create(name="Banana", quantity=10)

    def test_index_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_template_used(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_index_items_in_context(self):
        response = self.client.get(reverse('index'))
        self.assertTrue('items' in response.context)
        self.assertEqual(len(response.context['items']), 1)
