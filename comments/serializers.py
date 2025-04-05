from rest_framework import serializers
from .models import CommentReply, Comment, Report
from projects.models import Project

class CommentReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username instead of the user ID

    class Meta:
        model = CommentReply
        fields = ['id', 'comment', 'user', 'text', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'comment']

    def create(self, validated_data):
        # Get comment_id from the context and validate it
        comment_id = self.context.get('comment_id')
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise serializers.ValidationError("The specified comment does not exist.")
        
        # Set the comment in the validated data
        validated_data['comment'] = comment
        return super().create(validated_data)

    def validate_text(self, value):
        # Ensure the text is not empty
        if not value.strip():
            raise serializers.ValidationError("The reply text cannot be empty.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username instead of the user ID
    replies = CommentReplySerializer(many=True, read_only=True)  # Include replies

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'replies']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        # Get project_id from the context and validate it
        project_id = self.context.get('project_id')
        if not Project.objects.filter(id=project_id).exists():
            raise serializers.ValidationError("The specified project does not exist.")
        validated_data['project_id'] = project_id
        return super().create(validated_data)

    def validate_text(self, value):
        # Ensure the text is not empty
        if not value.strip():
            raise serializers.ValidationError("The comment text cannot be empty.")
        return value

class ReportSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username instead of the user ID
    project_name = serializers.SerializerMethodField()  # Custom field for project name
    comment_text = serializers.SerializerMethodField()  # Custom field for comment text
    comment_reply_text = serializers.SerializerMethodField()  # Custom field for comment reply text

    class Meta:
        model = Report
        fields = [
            'id', 'user', 'report_type', 'project', 'project_name', 
            'comment', 'comment_text', 'comment_reply', 'comment_reply_text', 
            'reason', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'user']

    def get_project_name(self, obj):
        # Return the project name if the report is related to a project
        return obj.project.title if obj.project else None

    def get_comment_text(self, obj):
        # Return the comment text if the report is related to a comment
        return obj.comment.text if obj.comment else None

    def get_comment_reply_text(self, obj):
        # Return the comment reply text if the report is related to a comment reply
        return obj.comment_reply.text if obj.comment_reply else None

    def validate(self, data):
        # Validate that only one of project, comment, or comment_reply is provided
        report_type = data.get('report_type')
        project = data.get('project')
        comment = data.get('comment')
        comment_reply = data.get('comment_reply')

        if report_type == 'project' and not project:
            raise serializers.ValidationError({"project": "A project must be specified for a project report."})
        if report_type == 'comment' and not comment:
            raise serializers.ValidationError({"comment": "A comment must be specified for a comment report."})
        if report_type == 'comment_reply' and not comment_reply:
            raise serializers.ValidationError({"comment_reply": "A comment reply must be specified for a comment reply report."})
        if sum(bool(x) for x in [project, comment, comment_reply]) > 1:
            raise serializers.ValidationError("You cannot report more than one type (project, comment, or comment reply) in the same report.")
        return data