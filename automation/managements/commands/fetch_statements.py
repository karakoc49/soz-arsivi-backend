import requests
from django.core.management.base import BaseCommand
from statements.models import Statement
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Fetch latest statements from example API and save them'

    def handle(self, *args, **kwargs):
        url = 'https://example.com/api/statements'  # Gerçek API URL'si ile değiştir

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stderr.write(f"Error fetching data: {e}")
            return

        data = response.json()
        for item in data:
            # Varsayılan yapıya göre mapping yap
            Statement.objects.update_or_create(
                external_id=item['id'],  # external_id alanını modelde ekle
                defaults={
                    'text': item['text'],
                    'date': parse_datetime(item['date']),
                    'source': item.get('source', ''),
                    # diğer alanlar
                }
            )
        self.stdout.write(self.style.SUCCESS('Statements updated successfully'))
