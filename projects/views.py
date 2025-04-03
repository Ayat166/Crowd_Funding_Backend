from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Rating, Project
from .serializers import RatingSerializer

class RatingListCreateView(APIView):
    """
    Handles listing all ratings for a project and creating a new rating.
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

        # Fetch and serialize ratings for the project
        ratings = Rating.objects.filter(project=project)
        serializer = RatingSerializer(ratings, many=True)

        # Include the average rating in the response
        response_data = {
            "avg_rating": project.avg_rating,  # Include the avg_rating from the Project model
            "ratings": serializer.data,       # Include the serialized ratings
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        # Validate that the project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {"error": "The specified project does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Pass the project instance to the serializer's context
        serializer = RatingSerializer(data=request.data, context={'request': request, 'project': project})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
