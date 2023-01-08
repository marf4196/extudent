from .serializers import MessageSerializer
from rest_framework import generics, viewsets
from django.db.models import Q
from ...models import Message
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


# class MessageGenericApiView(generics.ListCreateAPIView):
#     queryset = Message.objects.filter(is_recived=True)
#     serializer_class = MessageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         queryset = self.get_queryset()
#         obj = get_object_or_404(queryset, user=self.request.user)
#         return obj


class UserMessageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def list(self, request):
        queryset = Message.objects.filter(Q(is_recived=True)).filter(
            Q(reciver=self.request.user) | Q(writer=self.request.user)
        )
        serializer = self.serializer_class(data=queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.initial_data["writer"] = self.request.user
        serializer.initial_data["is_recived"] = False
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({"details": "invalid data"})
