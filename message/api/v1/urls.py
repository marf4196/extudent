from django.urls import path, include
from .views import MessageGenericApiView

urlpatterns = [
    ####
    path("userMessage",MessageGenericApiView.as_view(), name="userMessage"),
]
