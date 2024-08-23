import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv
import requests

# model import
from .models import Advocate, Company
from .serializers import AdvocateSerializer, CompanySerializer

# Load the env variable
load_dotenv()

TWITTER_URL = "https://api.twitter.com/2/users/by/username"

# Create your views here.
@api_view(['GET'])
def endpoints(request):
    print("twitter key" + os.environ.get('TWITTER_API_KEY'))
    data = ["/advocates", "advocates/:username"]
    return Response(data)


# Order of decorator matters
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def advocate_list(request):
    # Handle creation of advocate means POST request
    if request.method == 'GET':
        # Get the query params
        query = request.query_params.get('query')
        if query is None:
            query = ""

        data = Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
        serializer = AdvocateSerializer(data, many=True)
        return Response(serializer.data)

    # Handle creation of advocate means POST request
    if request.method == 'POST':
        new_advocate = Advocate.objects.create(
            username=request.data['username'],
            bio=request.data['bio']
        )
        serializer = AdvocateSerializer(new_advocate, many=False)
        return Response(serializer.data)


# Class based view
class AdvocateDetail(APIView):
    # Handle resource not found with more resilient code
    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            raise APIException("There was a problem!")

    def get(self, request, username):
        fields = 'user.fields=profile_image_url,description,public_metrics'
        endpoint = f'{TWITTER_URL}/{username}?{fields}'
        header = {
            'Authorization': 'Bearer ' + ''}
        try:
            response = requests.get(endpoint, headers=header).json()
        except Exception:
            raise APIException("There was a problem!")
        data = response['data']
        # Change size of the images
        data['profile_image_url'] = data['profile_image_url'].replace('normal', '400x400')
        # Update the advocate in the db
        advocate = self.get_object(username)
        advocate.name = data['name']
        advocate.profile_picture = data['profile_image_url']
        advocate.bio = data['description']
        advocate.twitter = "https://x.com/" + username
        advocate.save()
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    def put(self, request, username):
        data = self.get_object(username)
        data.username = request.username
        data.bio = request.bio
        data.save()
        serializer = AdvocateSerializer(data, many=False)
        return Response(serializer.data)


# Function based view
# @api_view(['GET', 'PUT', 'DELETE'])
# def advocate_details(request, username):
#     data = Advocate.objects.get(username=username)
#
#     if request.method == 'GET':
#         serializer = AdvocateSerializer(data, many=False)
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         data.username = request.username
#         data.bio = request.bio
#         data.save()
#         serializer = AdvocateSerializer(data, many=False)
#         return Response(serializer.data)
#
#     if request.method == 'DELETE':
#         data.delete()
#         return Response('User was deleted')


# Company Rest view logic
@api_view(['GET'])
def company_list(request):
    data = Company.objects.all()
    serializer = CompanySerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
def company_details(request, name):
    data = Company.objects.get(name=name)
    if request.method == 'GET':
        serializer = CompanySerializer(data, many=False)
        return Response(serializer.data)

    if request.method == 'PUT':
        data.name = request.name
        data.bio = request.bio
        serializer = CompanySerializer(data, many=True)
        return Response(serializer.data)