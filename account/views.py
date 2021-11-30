from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.response import Response

from .serializers import ChangePasswordSerializer, CustomUserSerializer,LoginSerializer
from django.contrib.auth import get_user_model

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

CustomUser = get_user_model()

@swagger_auto_schema(methods=['POST'], request_body=CustomUserSerializer())
@api_view(['POST'])
def signup_page(request):
        if request.method == 'POST':
    
            serializer = CustomUserSerializer(data = request.data)

            if serializer.is_valid(): 
                serializer.validated_data['password'] = make_password(serializer.validated_data['password']) #hash the password

                customuser = CustomUser.objects.create(**serializer.validated_data)
                
                serializer = CustomUserSerializer(customuser)

                data = {
                    "status"  : True,
                    "message":"success",
                    "data": serializer.data
                }
                return Response(data, status=status.HTTP_201_CREATED)

            else:
                error = {
                    'status'  : True,
                    'message':'Unsuccessful',
                    "errors": serializer.errors
                }       

                return Response(error, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
))
@api_view(['POST'])
def login_page(request):
    if request.method == 'POST':
        customuser = authenticate(request, username=request.data['username'], password=request.data['password'])
        if customuser is not None:
            if customuser.is_active==True:
                try:

                    customuser_detail = {}
                    customuser_detail['id']   = customuser.id
                    customuser_detail['first_name'] = customuser.first_name
                    customuser_detail['last_name'] = customuser.last_name
                    customuser_detail['email'] = customuser.email
                    customuser_detail['customusername'] = customuser.customusername
                    
                    user_logged_in.send(sender=customuser.__class__,
                                        request=request, customuser=customuser)

                    data = {
                    'status'  : True,
                    'message' : "Successful",
                    'data' : customuser_detail,
                    }
                    return Response(data, status=status.HTTP_200_OK)
                    
                except Exception as e:
                    raise e
            else:
            
                data = {
                    'status'  : False,
                    'error': 'This account has not been activated'
                }
            
            return Response(data,status=status.HTTP_403_FORBIDDEN)
        else:
            data = {
                'status'  : False,
                'error': 'Please provide a valid username and a password'
            }
        
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def get_user(request):
    if request.method == 'GET':
        customusers = CustomUser.objects.filter(is_active=True)

        serializer = CustomUserSerializer(customusers, many=True)

        data = {
            'status'  : True,
            "message":"success",
            "data": serializer.data
        }    #prepare the response

        return Response(data, status=status.HTTP_200_OK)




@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=CustomUserSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def customuser_detail(request, customuser_id):  

    try:
        customuser = CustomUser.objects.get(id = request.customuser.id, is_active=True) #get the data from the models
    except CustomUser.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }
        return Response(data, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = CustomUserSerializer(customuser)

        data = {
            "status"  : True,
            "message":"Successful",
            "data": serializer.data
        }  #prepare the response data

        return Response(data, status=status.HTTP_200_OK) #send the response

    elif request.method == 'PUT':
        serializer = CustomUserSerializer(customuser, data=request.data, partial=True)    

        if serializer.is_valid():
            if 'password' in serializer.validated_data.keys():
                raise ValidationError(detail="Cannot change password with this view")           
                
            serializer.save()
            data = {
                "status"  : True,
                "message":"Successful",
                "data": serializer.data
            }

            return Response(data, status=status.HTTP_202_ACCEPTED)

        else:
            data = {
                'status'  : False,
                'message':'Unsuccessful',
                "errors": serializer.errors
            }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customuser.is_active = False
        customuser.save()

        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, ststus=status.HTTP_204_NO_CONTENT)            


@swagger_auto_schema(methods=['POST'], request_body=ChangePasswordSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    # print(user.password)
    if request.method == "POST":
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if check_password(old_password, user.password):
                
                user.set_password(serializer.validated_data['new_password'])
                
                user.save()
                
                # print(user.password)
                
                return Response({"message":"success"}, status=status.HTTP_200_OK)
            
            else:
                error = {
                'message':'failed',
                "errors":"Old password not correct"
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST) 
            
        else:
            error = {
                'message':'failed',
                "errors":serializer.errors
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST) 