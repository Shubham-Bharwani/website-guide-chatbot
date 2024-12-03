from rest_framework import serializers

class AskSerializer(serializers.Serializer):
    query = serializers.CharField()
    scrape_context = serializers.CharField()
    # scrape_context = serializers.FileField()