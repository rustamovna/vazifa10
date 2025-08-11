from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Car
from .serializers import CarSerializer
from django.shortcuts import get_object_or_404

class CarListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarSerializer(car)
        return Response(serializer.data)

    def patch(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarSerializer(car, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
