from rest_framework import serializers
from .models import *

class ProjectImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['image']

class ProjectSerializer(serializers.ModelSerializer):
    images=ProjectImagesSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'

    def get_average_rating(self, obj):
        ratings=obj.ratings.all()
        if ratings.exists():
            return sum(r.score for r in ratings) / ratings.count()
        return 0