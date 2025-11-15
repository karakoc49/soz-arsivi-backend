from django.db import models
from parties.models import Party

class Politician(models.Model):
    class TitleChoices(models.TextChoices):
        MEMBER_OF_PARLIAMENT = "milletvekili", "Milletvekili"
        MAYOR = "belediye_baskani", "Belediye Başkanı"
        PARTY_LEADER = "genel_baskan", "Genel Başkan"
        PRESIDENT = "cumhurbaskani", "Cumhurbaşkanı"
        MINISTER = "bakan", "Bakan"
        SPOKESPERSON = "parti_sozcusu", "Parti Sözcüsü"
        CANDIDATE = "aday", "Aday"
        INDEPENDENT = "bagimsiz", "Bağımsız"
        OTHER = "diger", "Diğer"

    full_name = models.CharField(max_length=150)
    title = models.CharField(
        max_length=50,
        choices=TitleChoices.choices,
        default=TitleChoices.OTHER,
    )
    profile_url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='politicians/photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.get_title_display()})"


class PoliticianPartyMembership(models.Model):
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE, related_name='party_memberships')
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='members')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Politician Party Membership"
        verbose_name_plural = "Politician Party Memberships"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.politician.full_name} → {self.party.abbreviation} ({self.start_date} - {self.end_date or 'Günümüz'})"
