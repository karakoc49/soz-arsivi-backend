from django.db import models
from statements.models import Statement

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StatementTopic(models.Model):
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE, related_name='statement_topics')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='statements')

    class Meta:
        unique_together = ('statement', 'topic')

    def __str__(self):
        return f"{self.statement} → {self.topic.name}"