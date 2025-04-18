from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied



class RatingListCreateView(APIView):
    """
    Handles listing all ratings for a project and creating a new rating.
    """
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

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
    serializer_class = ProjectsSerializer
    parser_classes = [MultiPartParser, FormParser]  # Allows handling of image uploads
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()] # Allow anyone to view the list of projects
    

    def perform_create(self, serializer):
        print("Incoming data:", self.request.data)  # Debugging line
        serializer.save(creator=self.request.user)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [AllowAny]  # Allow anyone to view project details


class CancelProjectView(generics.UpdateAPIView):
    """Cancel project if donations are < 25% of total target."""
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        project = self.get_object()

        # Check if the requesting user is the creator of the project
        if project.creator != request.user:
            raise PermissionDenied("You do not have permission to cancel this project.")

        if project.is_below_25_percent():
            project.is_active = False  # Mark as canceled
            project.save()
            return Response({"message": "Project canceled due to low donations."}, status=status.HTTP_200_OK)

        return Response({"error": "Cannot cancel project. Donations are above 25%."}, status=status.HTTP_400_BAD_REQUEST)



class HomeProjectView (APIView):
    def get (self , request):
        latest_projects = Project.objects.all().order_by('-start_time')[:5]
        top_raited_projects = Project.objects.all().order_by('-avg_rating')[:5]
        featured_projects = Project.objects.filter(is_featured=True)[:5]
        data={
            'latest_projects':ProjectSerializer(latest_projects, many=True).data,
            'top_rated_projects':ProjectSerializer(top_raited_projects, many=True).data,
            'featured_projects':ProjectSerializer(featured_projects, many=True).data,
        }

        return Response(data)
    
def get_categories(request):
    categories = Category.objects.all().values("id", "name")
    return JsonResponse(list(categories), safe=False)

def category_projects(request, category_id):
    category = Category.objects.get(id=category_id)
    projects = Project.objects.filter(category=category)
    serialized_projects = ProjectSerializer(projects, many=True).data
    return JsonResponse({'projects': serialized_projects}, safe=False)

class SearchProjectsView(APIView):
    def get(self, request):
        search_term = request.GET.get('query', '').strip()  #search term from query parameters
        print(f"Search query: {search_term}")

        projects = Project.objects.all()

        if search_term:
            projects = projects.filter(
                Q(tags__icontains=search_term) | 
                Q(category__name__icontains=search_term) 
            )

            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        if not projects: 
            return JsonResponse({'message': 'No projects found for this category'}, status=200)
        return JsonResponse({'projects': list(projects.values())})


class AdminFeatureProjectView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can access this view

    def get(self, request):
        projects = Project.objects.all()
        data = [{'id': project.id, 'title': project.title, 'is_featured': project.is_featured} for project in projects]
        return Response(data)

    def post(self, request):
        project_id = request.data.get('project_id')
        is_featured = request.data.get('is_featured')

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        project.is_featured = is_featured
        project.save()
        return Response({'message': f'Project "{project.title}" updated to featured = {is_featured}'}, status=status.HTTP_200_OK)
    
class ProjectFeatureUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]  

    def patch(self, request, *args, **kwargs):
        project = self.get_object()
        is_featured = request.data.get("featured")

        if is_featured is None:
            return Response({"error": "Missing 'featured' field."}, status=status.HTTP_400_BAD_REQUEST)

        project.featured = is_featured
        project.save()
        serializer = self.get_serializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)