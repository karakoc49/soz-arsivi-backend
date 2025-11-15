from rest_framework import serializers
from .models import Statement
from politicians.serializers import PoliticianSerializer
from topics.serializers import TopicSerializer

class StatementSerializer(serializers.ModelSerializer):
    politician = PoliticianSerializer(read_only=True)
    politician_id = serializers.PrimaryKeyRelatedField(
        queryset=Statement.objects.model.politician.field.related_model.objects.all(),
        source='politician',
        write_only=True
    )
    topics = TopicSerializer(many=True, read_only=True)
    ai = serializers.SerializerMethodField()

    class Meta:
        model = Statement
        fields = [
            'id', 'statement_type', 'content', 'media_file', 'media_sha256',
            'source', 'published_at', 'created_at',
            'politician', 'politician_id', 'topics', 'ai'
        ]

    def get_ai(self, obj):
        return {
            "sentiment": obj.ai_sentiment,
            "keywords": obj.ai_keywords,
            "summary": obj.ai_summary,
            "language": obj.ai_language
        }
