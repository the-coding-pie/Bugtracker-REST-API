from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import serializers

# GET /api/v1/users/me/
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    try:
        user = UserSerializer(request.user, context={"request": request}).data
        return Response({
                'user': user
            })
    except:
        return Response({
            'detail': 'Oops, something went wrong.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# POST /api/v1/users/login/
@api_view(['POST'])
def login_user(request):
    try:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token, created = Token.objects.get_or_create(user=serializer.validated_data)
            return Response({
                'token': token.key
            })
    except serializers.ValidationError:
        if serializer.errors.get('non_field_errors', None):
            return Response({
            'detail': serializer.errors['non_field_errors'][0],
        }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'details': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({
            'detail': 'Oops, something went wrong.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# POST /api/v1/users/register/
@api_view(['POST'])
def register_user(request):
    try:
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({
                'token': token.key,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'details': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({
            'detail': 'Oops, something went wrong.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        request.user.auth_token.delete()
        return Response({
            'detail': 'You have been logged out.'
        },status=status.HTTP_200_OK)
    except:
        return Response({
            'detail': 'Oops, something went wrong.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)