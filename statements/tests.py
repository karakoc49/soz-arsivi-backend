from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from politicians.models import Politician
from .models import Statement
import datetime

class StatementAPITest(APITestCase):

    def setUp(self):
        # Politician oluştur
        self.politician = Politician.objects.create(
            full_name="Test Politician",
            title="milletvekili",
            profile_url="http://example.com",
            active=True,
        )

        # Statement oluştur
        self.statement1 = Statement.objects.create(
            politician=self.politician,
            statement_type='text',
            content="Bu bir test açıklamasıdır.",
            published_at=datetime.datetime(2024, 1, 1, 12, 0),
            source="http://source.com",
        )
        self.statement2 = Statement.objects.create(
            politician=self.politician,
            statement_type='image',
            content="",
            published_at=datetime.datetime(2025, 1, 1, 12, 0),
            source="http://source.com",
        )

    def test_list_statements(self):
        url = reverse('statement-list')  # urls.py'de basename=statement varsayımı
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_filter_by_politician(self):
        url = reverse('statement-list')
        response = self.client.get(url, {'politician': self.politician.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_filter_by_statement_type(self):
        url = reverse('statement-list')
        response = self.client.get(url, {'statement_type': 'image'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['statement_type'], 'image')

    def test_ordering(self):
        url = reverse('statement-list')
        response = self.client.get(url, {'ordering': 'published_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['results'][0]['published_at'] < response.data['results'][1]['published_at'])
