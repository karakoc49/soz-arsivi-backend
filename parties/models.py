from django.db import models

class Party(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    color_code = models.CharField(max_length=7, blank=True, null=True)  # Örn: #FF0000

    def __str__(self):
        return self.name
