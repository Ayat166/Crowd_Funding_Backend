from rest_framework import serializers
from .models import Project, ProjectImage, Category

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    donation = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'details',
            'category',
            'total_target',
            'tags',
            'start_time',
            'end_time',
            'is_active',
            'images',
            'donation',
            'duration',
            'created_at'
        ]

    def get_donation(self, obj):
        return sum(d.amount for d in obj.donations.all())

    def get_duration(self, obj):
        if obj.start_time and obj.end_time:
            return (obj.end_time - obj.start_time).days
        return None
