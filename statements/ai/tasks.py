from celery import shared_task
from statements.models import Statement
from .processor import analyze_statement

# statements/ai/tasks.py
@shared_task
def analyze_statement_task(statement_id):
    statement = Statement.objects.get(id=statement_id)
    result = analyze_statement(statement.content)
    # Save results
    statement.ai_sentiment = result["sentiment"]
    statement.ai_keywords = result["keywords"]
    statement.ai_summary = result["summary"]
    statement.ai_language = result["language"]
    statement.save()