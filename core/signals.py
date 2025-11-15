from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from parties.models import Party
from politicians.models import Politician
from statements.models import Statement
from topics.models import Topic

@receiver([post_save, post_delete], sender=Party)
@receiver([post_save, post_delete], sender=Politician)
@receiver([post_save, post_delete], sender=Statement)
@receiver([post_save, post_delete], sender=Topic)
def clear_cache_on_change(sender, **kwargs):
    cache.clear()
