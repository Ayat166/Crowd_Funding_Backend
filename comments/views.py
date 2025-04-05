from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Comment, CommentReply, Report
from .serializers import CommentSerializer, CommentReplySerializer, ReportSerializer
from projects.models import Project  # Import the Project model

# Create your views here.

class CommentListCreateView(APIView):
    """
    Handles listing all comments for a project and creating a new comment.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        # Validate that the project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {"error": "The specified project does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Fetch and serialize comments for the project
        comments = Comment.objects.filter(project=project)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        serializer = CommentSerializer(data=request.data, context={'project_id': project_id})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentReplyCreateView(APIView):
    """
    Handles creating a reply to a comment.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        serializer = CommentReplySerializer(data=request.data, context={'comment_id': comment_id})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportListCreateView(APIView):
    """
    Handles listing all reports and creating a new report.
    """
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]  # Only admin users can access GET
        return [IsAuthenticated()]  # Authenticated users can access POST

    def get(self, request):
        # List all reports
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a new report
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            # Save the report before accessing serializer.data
            report = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
