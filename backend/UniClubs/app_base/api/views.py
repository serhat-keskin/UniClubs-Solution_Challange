from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.core.files.base import ContentFile  #file handle
import requests, json, copy, datetime, traceback
from django.utils import timezone


from rest_framework.response import Response
from app_base import models as gdsc_app_base_models
# from .serializers import RoomSerializer
from . import serializers as gdsc_app_base_serializers


from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from .serializers import serializers_for_all
from rest_framework.generics import GenericAPIView,ListCreateAPIView, RetrieveUpdateDestroyAPIView,get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.exceptions import ValidationError
from rest_framework import permissions

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email #email to be encrypted into the token
        token['name'] = user.name #name to be encrypted into the token
        token['surname'] = user.surname #surname to be encrypted into the token
        token['is_admin'] = user.is_staff #is_admin to be encrypted into the token
        

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['GET'])# this just takes a list of http methods that we can send-you can also set put, delete or etc   
def getRoutes(request): #we will get back a access and refresh token
    routes=[
        '/api/token',
        '/api/token/refresh' #this route gives a new token based on a refresh token that you sent 
    ]
    return JsonResponse(routes,safe=False) 

#ekledim


#region    eski (rest framework kullanmadan)
def getRoutesOld(request):
    routes=[
        'GET /api',
        'GET /api/rooms/',
        'GET /api/rooms/:id/',
    ]
    return JsonResponse(routes,safe=False)
#endregion

@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/clubs/',
        'GET /api/clubs/:id/',
    ]
    return Response(routes)

@api_view(['GET'])
def getClubs(request):
    clubs = gdsc_app_base_models.Club.objects.all()
    serializer = gdsc_app_base_serializers.ClubSerializer(clubs,many=True)
    # response = []
    # for club in clubs:
    #     temp={"name":club.name,"description":club.description,"image":club.logo.url}
    #     response.append(temp)
    # print(response)
    # return Response(response)
    return Response(serializer.data)

@api_view(['GET'])
def getClub(request,pk):
    club = gdsc_app_base_models.Club.objects.get(id=pk)
    serializer = gdsc_app_base_serializers.ClubSerializer(club,many=False)
    return Response(serializer.data)
#make rest_framework concrete view classes



## İNCELENECEK ## #TODO
views = {}
for model, serializer in serializers_for_all.items():
    class_name = model.__name__ + 'View'
    view_class = type(class_name, (RetrieveUpdateDestroyAPIView,), {'serializer_class': serializer, 'queryset': model.objects.all(), 'permission_classes': [permissions.IsAuthenticated]})
    views[model] = view_class
