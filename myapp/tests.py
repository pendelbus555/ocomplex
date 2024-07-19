from django.test import TestCase, Client
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import SearchHistory


class CitySearchCountAPITests(APITestCase):
    def setUp(self):
        SearchHistory.objects.create(session_key='123', query='London')
        SearchHistory.objects.create(session_key='124', query='London')
        SearchHistory.objects.create(session_key='125', query='Paris')

    def test_get_city_search_count(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['query'], 'London')
        self.assertEqual(response.data[0]['count'], 2)
        self.assertEqual(response.data[1]['query'], 'Paris')
        self.assertEqual(response.data[1]['count'], 1)


class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/index.html')
        self.assertIn('form', response.context)

    def test_post_index_view_valid_city(self):
        response = self.client.post(reverse('index'), {'city_name': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SearchHistory.objects.filter(query='London').exists())
        self.assertEqual(response.cookies['last_city'].value, 'London')
