from rest_framework import serializers
from .models import Topic, StatementTopic

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']

class StatementTopicSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    topic_id = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all(), source='topic', write_only=True)

    class Meta:
        model = StatementTopic
        fields = ['id', 'statement', 'topic', 'topic_id']
