from rest_framework import serializers
from .models import Rating

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
from .models import Project, ProjectImage

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'  # Include all fields

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'
