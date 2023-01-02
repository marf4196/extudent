from .serializer import OrderSerializer
from rest_framework import generics
from ...models import Orders
from rest_framework import permissions
from django.shortcuts import get_object_or_404


class OrdersListGenericApiView(generics.ListCreateAPIView):
    queryset = Orders.objects.filter(status=False)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user = self.request.user)
        return obj
    
class OrdersDeleteGenericApiView(generics.RetrieveDestroyAPIView):
    queryset = Orders.objects.filter(status=False)
    permission_classes = [permissions.IsAuthenticated]
    erializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user = self.request.user)
        return obj