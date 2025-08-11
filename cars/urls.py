from django.urls import path
from .views import CarListCreateAPIView, CarDetailAPIView

urlpatterns = [
    path('', CarListCreateAPIView.as_view(), name='car-list-create'),
    path('<int:pk>/', CarDetailAPIView.as_view(), name='car-detail'),
]
