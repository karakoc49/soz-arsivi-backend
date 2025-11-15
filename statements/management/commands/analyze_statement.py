from django.core.management.base import BaseCommand
from statements.ai.tasks import analyze_statement_task

class Command(BaseCommand):
    help = 'Run analyze_statement_task for given statement id'

    def add_arguments(self, parser):
        parser.add_argument('statement_id', type=int, help='ID of the statement to analyze')

    def handle(self, *args, **options):
        statement_id = options['statement_id']
        result = analyze_statement_task.delay(statement_id)
        self.stdout.write(self.style.SUCCESS(f"Task {result.id} gönderildi."))
