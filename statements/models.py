from django.core.exceptions import ValidationError
from django.db import models
from politicians.models import Politician
from django.db.models.signals import post_save
from django.dispatch import receiver

import hashlib
import uuid
import os

def statement_media_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("statements", filename)


class Statement(models.Model):
    STATEMENT_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('link', 'Link'),
    )

    politician = models.ForeignKey(Politician, on_delete=models.CASCADE, related_name='statements')
    statement_type = models.CharField(max_length=20, choices=STATEMENT_TYPES)
    content = models.TextField(blank=True, null=True)
    media_file = models.FileField(upload_to=statement_media_path, blank=True, null=True)
    media_sha256 = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    ai_sentiment = models.CharField(max_length=20, blank=True, null=True)  # positive, neutral, negative
    ai_keywords = models.JSONField(blank=True, null=True)  # ["ekonomi", "enflasyon", "asgari ücret"]
    ai_summary = models.TextField(blank=True, null=True)  # AI ile oluşturulmuş kısa özet
    ai_language = models.CharField(max_length=20, blank=True, null=True)  # tr, en, vs.
    external_id = models.CharField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.politician.full_name} - {self.statement_type} - {self.published_at.date()}"

    def save(self, *args, **kwargs):
        if self.media_file:
            hasher = hashlib.sha256()
            for chunk in self.media_file.file.chunks():
                hasher.update(chunk)
            self.media_sha256 = hasher.hexdigest()
        super().save(*args, **kwargs)

    def clean(self):
        if self.statement_type == 'text':
            if not self.content:
                raise ValidationError('Text tipi açıklama için content alanı boş olamaz.')
            if self.media_file:
                raise ValidationError('Text tipi açıklama için media_file alanı boş olmalı.')
        elif self.statement_type in ['image', 'video']:
            if not self.media_file:
                raise ValidationError(f'{self.statement_type} tipi açıklama için media_file alanı zorunludur.')
            if self.content:
                # Opsiyonel, ama içerik alanını boş bırakmak isteyebilirsin
                pass
        elif self.statement_type == 'link':
            if not self.content:
                raise ValidationError('Link tipi açıklama için content alanı boş olamaz.')

        super().clean()

@receiver(post_save, sender=Statement)
def run_analysis_after_statement_save(sender, instance, created, **kwargs):
    from statements.ai.tasks import analyze_statement_task
    # Yeni statement eklendiğinde Celery task'ı tetikle
    analyze_statement_task.delay(instance.id)