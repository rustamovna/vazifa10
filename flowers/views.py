from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Flower
from .serializers import FlowerSerializer
from django.shortcuts import get_object_or_404

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class FlowerListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        flowers = Flower.objects.all()
        serializer = FlowerSerializer(flowers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FlowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FlowerDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        flower = get_object_or_404(Flower, pk=pk)
        serializer = FlowerSerializer(flower)
        return Response(serializer.data)

    def patch(self, request, pk):
        flower = get_object_or_404(Flower, pk=pk)
        serializer = FlowerSerializer(flower, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        flower = get_object_or_404(Flower, pk=pk)
        flower.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)