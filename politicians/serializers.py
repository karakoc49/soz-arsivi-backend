from rest_framework import serializers

from parties.models import Party
from .models import Politician, PoliticianPartyMembership
from parties.serializers import PartySerializer

class PoliticianPartyMembershipSerializer(serializers.ModelSerializer):
    party = PartySerializer(read_only=True)
    party_id = serializers.PrimaryKeyRelatedField(queryset=Party.objects.all(), source='party', write_only=True)

    class Meta:
        model = PoliticianPartyMembership
        fields = ['id', 'party', 'party_id', 'start_date', 'end_date']

class PoliticianSerializer(serializers.ModelSerializer):
    party = serializers.SerializerMethodField()
    party_memberships = PoliticianPartyMembershipSerializer(many=True, read_only=True)

    class Meta:
        model = Politician
        fields = ['id', 'full_name', 'title', 'profile_url', 'active', 'party', 'party_memberships', 'photo']

    def get_party(self, obj):
        membership = obj.party_memberships.filter(end_date__isnull=True).first()
        if membership:
            return PartySerializer(membership.party).data
        return None
