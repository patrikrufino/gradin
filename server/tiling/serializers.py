from rest_framework import serializers

class PosterSerializer(serializers.Serializer):
    pdf_file = serializers.FileField()
    rows = serializers.IntegerField()
    cols = serializers.IntegerField()
