from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models
from .models import *
from .serializers import *
from django.http import JsonResponse
<<<<<<< HEAD
from django.db.models import Q
=======
>>>>>>> f7dc5ade48e5196033bf9d0412c12132acaa8959

class HomeProjectView (APIView):
    def get (self , request):
        latest_projects = Project.objects.all().order_by('-start_time')[:5]
        top_raited_projects = Project.objects.all().order_by('-ratings')[:5]
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
<<<<<<< HEAD
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
=======
    if not projects: return JsonResponse({'message': 'No projects found for this category'}, status=200)
    return JsonResponse({'projects': list(projects.values())})
>>>>>>> f7dc5ade48e5196033bf9d0412c12132acaa8959
