from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from authentication.serializers import RegisterSerializer, LoginSerializer, AuthUserSerializer
from django.contrib.auth import authenticate

class AuthUserAPIView(GenericAPIView):

    serializer_class = AuthUserSerializer
    permissions_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return response.Response({"user": serializer.data})

class RegisterAPIView(GenericAPIView):
    
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response.Response({"message":"user created successfully", "user": serializer.data}, status = status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(GenericAPIView):
    
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        username    = request.data.get('username',)
        password = request.data.get('password',)
        user = authenticate(username = username, password = password)

        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status = status.HTTP_200_OK)

        return response.Response({"message": "invalid credentials, try again"}, status = status.HTTP_401_UNAUTHORIZED)