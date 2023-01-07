from .serializer import ListCreateDeleteOrderSerializer
from rest_framework import viewsets, generics

from ...models import Orders
from accounts.models import Profile, UserIdentDocs

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status




class OrdersListApiView(viewsets.ViewSet):
    queryset = Orders.objects.filter(status=False)
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = ListCreateDeleteOrderSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            owner = self.request.data["owner"]
            serializer.save()
            profile_obj= Profile.objects.get(user=owner)
            return Response({"detail": "order created"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        delete_queryset = Orders.objects.filter(owner=self.request.user).filter(status=False)
        order_obj = get_object_or_404(delete_queryset, pk=pk)
        serializer = self.serializer_class(order_obj)
        owner = self.request.user
        profile_obj= Profile.objects.get(user=owner)
        order_obj.delete()
        
        return Response({"detail": "order deleted call the admin and wait for your money back"})

    def retrive(self, request, pk=None):
        order_obj = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(order_obj)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        order_obj = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(order_obj, data=request.data)
        buyer = self.request.user
        buyer_identity = UserIdentDocs.objects.get(user=buyer)
        
        if buyer != order_obj.owner:
            if buyer_identity.is_complete == True:
                buyer_profile = Profile.objects.get(user=buyer)
                if  serializer.is_valid(raise_exception=True):
                    serializer.data["status"] = request.data["status"]
                    if buyer_profile.ballance >= (order_obj.price * order_obj.amount):
                        buyer_profile.ballance -= (order_obj.price * order_obj.amount)
                        serializer.save()
                        buyer_profile.save()
                    else:
                        return Response({"details":"you should deposit into your wallet first, not enough money"})
                else:
                    return Response({"details":"data is invalid"})
            else:
                return Response({"details":"you must upload your own identity docs"})
        else:
            return Response({"details":"you dont have access to update this order"})
            

