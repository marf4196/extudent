from .serializers import MessageSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q

from accounts.models import User
from ...models import Message


from rest_framework import generics, permissions, viewsets, renderers
from rest_framework.response import Response

# user messages viewset
###############################################################
class UserMessageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer
    
    def list(self,request):
        queryset = Message.objects.filter(Q(writer=self.request.user) | Q(is_recived=True))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self,request):
        
        serializer = self.serializer_class(data=request.data)
        serializer.initial_data["writer"] = self.request.user.pk
        serializer.initial_data["reciver"]=""
        serializer.initial_data["is_recived"]= False
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"datail":"message sent to admin"})
        else:
            return Response({"datail":"data is invalid"})
# view for writing and sending messages too all users by admin
###############################################################

class AdminMessageViewSet(viewsets.ViewSet):
    
    serilizer_class = MessageSerializer
    renderer_classes = (renderers.BrowsableAPIRenderer,renderers.JSONRenderer, renderers.HTMLFormRenderer)
    permission_classes =[permissions.IsAdminUser]
    
    def list(self, request):
        message_queryset = Message.objects.filter(is_recived=False)
        serializer = self.serilizer_class(message_queryset, many=True)
        return Response(serializer.data)
    def create(self, request):
        writer_admin = self.request.user
        serializer = self.serilizer_class(data=request.data)
        serializer.initial_data["writer"] = writer_admin.pk
        serializer.initial_data["reciver"]=""
        serializer.initial_data["is_recived"]= True
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail":"your message sent to all active users"})
        else:
            return Response({"detail":"data is not valid"})