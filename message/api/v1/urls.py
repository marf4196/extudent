from django.urls import path, include
from .views import UserMessageViewSet

urlpatterns = [
    ####
    path("userMessage/",UserMessageViewSet.as_view({"get":"list","post":"create"}), name="userMessage"),
]
