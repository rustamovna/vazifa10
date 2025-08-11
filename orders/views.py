from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Order
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404

class OrderListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_staff:
            orders = Order.objects.all().order_by('-ordered_at')
        else:
            orders = Order.objects.filter(user=user).order_by('-ordered_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.user != request.user and not request.user.is_staff:
            return Response({'detail': 'You do not have permission to view this order.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.user != request.user and not request.user.is_staff:
            return Response({'detail': 'You do not have permission to edit this order.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.user != request.user and not request.user.is_staff:
            return Response({'detail': 'You do not have permission to delete this order.'}, status=status.HTTP_403_FORBIDDEN)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
