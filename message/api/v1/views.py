from .serializers import MessageSerializer
from rest_framework import generics
from ...models import Message
from rest_framework import permissions
from django.shortcuts import get_object_or_404


class MessageGenericApiView(generics.ListCreateAPIView):
    queryset = Message.objects.filter(is_recived=True)
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
        