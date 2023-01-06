from django.urls import path, include
from .views import AdminMessageViewSet,UserMessageViewSet

urlpatterns = [
    # admin sends a message to all users
    path("message/admin/create/",AdminMessageViewSet.as_view({"post":"create","get":"list"}), name="adminMessage"),
    # users can send a message to admin and see their recived messages
    path("profile/message/",UserMessageViewSet.as_view({"post":"create","get":"list"}), name="userMessage"),
]
