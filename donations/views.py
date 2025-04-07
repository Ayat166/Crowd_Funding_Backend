from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Donation
from .serializers import Donation_Serializer
from projects.models import Project  # Import the Project model

class DonationListCreateView(APIView):
    """
    Handles listing all donations and creating a new donation.
    """
    permission_classes = [IsAuthenticated]  # Require authentication for this view

    def get(self, request):
        # Restrict access to admin users only
        if not request.user.is_staff:  # Check if the user is an admin
            return Response(
                {"error": "You do not have permission to access this resource."},
                status=status.HTTP_403_FORBIDDEN
            )

        donations = Donation.objects.all()
        serializer = Donation_Serializer(donations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Donation_Serializer(data=request.data)
        if serializer.is_valid():
            #print("Valid data received:", serializer.validated_data)  # Debugging line
            project = serializer.validated_data['project']
            donation_amount = serializer.validated_data['amount']

            # Check if the donation exceeds the remaining target
            if donation_amount > (project.total_target - project.total_donations):
                return Response(
                    {"error": f"Donation exceeds the remaining target of {project.total_target - project.total_donations:.2f}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save the donation and update the project's total donations
            serializer.save(user=request.user)  # Associate the donation with the authenticated user
            project.total_donations += donation_amount
            project.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDonationListView(APIView):
    """
    Handles listing all donations for a specific project.
    """
    permission_classes = [IsAuthenticated]  # Require authentication for this view

    def get(self, request, project_id):
        # Validate that the project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {"error": "The specified project does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Fetch and serialize donations for the project
        donations = Donation.objects.filter(project=project)
        serializer = Donation_Serializer(donations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)