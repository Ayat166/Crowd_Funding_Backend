from rest_framework import serializers
from .models import *
from users.serializers import UserSerializer
class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username instead of the user ID
    class Meta:
        model = Rating
        fields = ['id', 'user', 'project', 'score']
        read_only_fields = ['id', 'user', 'project']  # Make 'project' read-only

    def validate_score(self, value):
        # Ensure the score is between 1 and 5
        if value < 1 or value > 5:
            raise serializers.ValidationError("The rating score must be between 1 and 5.")
        return value

    def create(self, validated_data):
        # Get project from the context and add it to validated_data
        project = self.context.get('project')
        validated_data['project'] = project
        return super().create(validated_data)
    
    def validate(self, data):
        # Ensure the user has not already rated the project
        user = self.context['request'].user
        project = self.context.get('project')
        if Rating.objects.filter(user=user, project=project).exists():
            raise serializers.ValidationError("You have already rated this project.")
        return data

class ProjectImagesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = ProjectImage
        fields = ['id','image']
        
class ProjectsSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True
    )
    uploaded_images = ProjectImagesSerializer(source='images', many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    creator = UserSerializer(read_only=True) 

    class Meta:
        model = Project
        fields = ['id', 'title', 'details', 'category', 'creator', 'is_active', 
                  'total_target', 'total_donations', 'images', 'uploaded_images','avg_rating','current_donations','start_time','end_time','tags','is_featured']


    def create(self, validated_data):
        images = validated_data.pop('images', [])
        validated_data['is_active'] = True
        project = Project.objects.create(**validated_data)
        for image in images:
            ProjectImage.objects.create(project=project, image=image)
        return project



class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'



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


class ProjectUserImageSerializer(serializers.ModelSerializer):
     class Meta:
         model = ProjectImage
         fields = ['image']

class CategoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProjectUserSerializer(serializers.ModelSerializer):
    images = ProjectUserImageSerializer(many=True, read_only=True)
    category = CategoryUserSerializer(read_only=True)
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
