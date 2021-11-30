from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import to_do_list

from .serializers import To_do_listSerializer
from .models import To_do_list
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

@swagger_auto_schema(methods=['POST'], request_body=To_do_listSerializer())
@api_view(['GET', 'POST'])
def To_do_list(request):             

    if request.method == 'GET':
        all_to_do_list = To_do_list.objects.all() #get the data

        serializer = To_do_listSerializer(all_to_do_list, many=True)
        #serialize the data

        data = {
            "message":"success",
            "data": serializer.data
        }    #prepare the response
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        serializer = To_do_listSerializer(data=request.data) #get and deserialize the data

        if serializer.is_valid(): #check if data is valid
            serializer.save() #save the data
            data = {
                "message":"success",
                "data": serializer.data
            }
            return Response({}, status=status.HTTP_200_OK)

        else:
            error = {
                'message':'failed',
                "errors": serializer.errors
            }       

            return Response(error, status=status.HTTP_400_BAD_REQUEST)

 
@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=To_do_listSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
def to_do_list_detail(request, to_do_list_id):
    
    try:
        to_do_list = To_do_list.objects.get(id=to_do_list_id) #get the data from the models
    except To_do_list.DoesNotExist:
        error = {
            'message':'failed',
            "errors": f"To_do_list with id {to_do_list_id} does not exist"
           }
        
        return Response(error, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = To_do_listSerializer(to_do_list)

        data = {
            "message":"success",
            "data": serializer.data
        }  #prepare the response data

        return Response(data, status=status.HTTP_200_OK) #send the response

    elif request.method == 'PUT':
        serializer = To_do_listSerializer(to_do_list, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = {
                "message":"success",
                "data": serializer.data
            }

            return Response(data, status=status.HTTP_202_ACCEPTED)

        else:
            error = {
                'message':'failed',
                "errors": serializer.errors
            }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        to_do_list.delete()

        return Response({"message":"success"}, ststus=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def to_do_list(request):
    if request.method == 'GET':
        to_dos = To_do_list.objects.values_list('to_do', flat=True).distinct()

        print(to_dos)

        data = {to_do:{
            "count":To_do_list.objects.filter(to_do=to_do).count(),
            "data":To_do_list.objects.filter(to_do=to_do).values()
            }

                for to_do in to_dos}

        return Response(data, status=status.HTTP_200_OK)

    # def test_view(request):
    #     my_to_dos = To_do_list.objects.all()
    # #print(my_to_dos)

    # data = {'to_dos':my_to_dos}

    # return render(request, data)
