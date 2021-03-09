from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from Countries.models import Countries
from Countries.seriallizers import CountriesSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET','POST'])
def countries_list(request):
    if request.method == 'GET':
        contrees = Countries.objects.all()
        
        name = request.GET.get('name', None)
        if name is not None:
            contrees = Countries.filter(name_icontains=name)
            
        contrees_serializer = CountriesSerializer(contrees, many=True)
        return JsonResponse(contrees_serializer.data, safe=False)
        # safe-False for object serialization
        
    elif request.method == 'POST':
        contrees_data = JSONParser().parse(request)
        contrees_serializer = CountriesSerializer(data=contrees_data)
        if contrees_serializer.is_valid():
            contrees_serializer.save()
            return JsonResponse(contrees_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(contrees_serializer.errors, status=status.HTTP_400_BAD_REQUEST)         
        
        
@api_view(['GET','PUT', 'DELETE'])
def countries_detail(request, pk):
    try:
        contrees = Countries.objects.get(pk=pk)
    except Countries.DoesNotExist:
        return JsonResponse({'message': 'The Country does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        contrees_serializer = CountriesSerializer(contrees)
        return JsonResponse(contrees_serializer.data)
        
    elif request.method == 'PUT':
        contrees_data = JSONParser().parse(request)
        contrees_serializer = CountriesSerializer(contrees, data=contrees_data)
        if contrees_serializer.is_valid():
            contrees_serializer.save()
            return JsonResponse(contrees_serializer.data)
        return JsonResponse(contrees_serializer.errors, status=status.HTTP_400_BAD_REQUEST)         
    
    elif request.method == 'DELETE':
        contrees.delete()
        return JsonResponse({'message': 'Country was deleted successfully'}, status=status.HTTP_204_NO_CONTENT)