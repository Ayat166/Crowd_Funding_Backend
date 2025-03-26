from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models
from .models import *
from .serializers import *

# Create your views here.
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
