from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Rating, Project
from .serializers import RatingSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render, get_object_or_404, redirect
from .serializers import ProjectSerializer
from .forms import ProjectForm  # Ensure you create this form in `forms.py`
from rest_framework.parsers import MultiPartParser, FormParser



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

# API Views
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can create projects
    parser_classes = [MultiPartParser, FormParser]  # Allows handling of image uploads

    def perform_create(self, serializer):
        # Automatically set the creator to the logged-in user
        serializer.save(creator=self.request.user)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]  # Just for testing, change later to [IsAuthenticated]

class CancelProjectView(generics.UpdateAPIView):
    """Cancel project if donations are < 25% of total target."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if project.is_below_25_percent():
            project.is_active = False  # Mark as canceled
            project.save()
            return Response({"message": "Project canceled due to low donations."}, status=status.HTTP_200_OK)
        return Response({"error": "Cannot cancel project. Donations are above 25%."}, status=status.HTTP_400_BAD_REQUEST)

# Function-Based Views for Frontend
def project_list_view(request):
    projects = Project.objects.all()
    return render(request, "projects/project_list.html", {"projects": projects})

def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "projects/project_detail.html", {"project": project})

def project_create_view(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("project-list")
    else:
        form = ProjectForm()
    return render(request, "projects/project_form.html", {"form": form})
