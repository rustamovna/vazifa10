from django.urls import path
from .views import RegisterView, FlowerListCreateAPIView, FlowerDetailAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', FlowerListCreateAPIView.as_view(), name='flower-list-create'),
    path('<int:pk>/', FlowerDetailAPIView.as_view(), name='flower-detail'),
]
