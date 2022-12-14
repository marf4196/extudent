from .serializer import ListCreateDeleteOrderSerializer, WithdrawSerializer
from rest_framework import viewsets, generics

from ...models import Orders, Withdraw
from accounts.models import Profile, UserIdentDocs

from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status


class OrdersListApiView(viewsets.ViewSet):
    queryset = Orders.objects.filter(status=False)
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = ListCreateDeleteOrderSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            owner = self.request.data["owner"]
            serializer.data["owner"] = self.request.data["owner"]
            return Response({"detail": "order created"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        delete_queryset = Orders.objects.filter(owner=self.request.user).filter(
            status=False
        )
        order_obj = get_object_or_404(delete_queryset, pk=pk)
        serializer = self.serializer_class(order_obj)
        owner = self.request.user
        profile_obj = Profile.objects.get(user=owner)
        order_obj.delete()

        return Response(
            {"detail": "order deleted call the admin and wait for your money back"}
        )

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
                if serializer.is_valid(raise_exception=True):
                    serializer.data["status"] = request.data["status"]
                    if buyer_profile.ballance >= (order_obj.price * order_obj.amount):
                        buyer_profile.ballance -= order_obj.price * order_obj.amount
                        serializer.save()
                        buyer_profile.save()
                    else:
                        return Response(
                            {
                                "details": "you should deposit into your wallet first, not enough money"
                            }
                        )
                else:
                    return Response({"details": "data is invalid"})
            else:
                return Response({"details": "you must upload your own identity docs"})
        else:
            return Response({"details": "you dont have access to update this order"})


class UserCompletedOrders(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ListCreateDeleteOrderSerializer

    def list(self, request):
        queryset = Orders.objects.filter(
            Q(owner=self.request.user) | Q(buyer=self.request.user)
        ).filter(Q(status=True))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrive(self, request, pk=None):
        queryset = Orders.objects.filter(
            Q(owner=self.request.user) | Q(buyer=self.request.user)
        ).filter(Q(status=True, pk=pk))
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


class Withdraw(viewsets.ViewSet):
    # creating class for requesting withdraw
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WithdrawSerializer

    def list(self, request):
        queryset = Withdraw.objects.filter(user=self.request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        profile_obj = Profile.objects.get(pk=self.request.user)
        serializer = self.serializer_class(request.data)
        if serializer.initial_data["amount"] >= profile_obj.ballance:
            serializer.data["user"] = self.request.user
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"details": "withdraw request sent sucssesfully"})
            else:
                return Response({"details": "invalid data"})
        else:
            return Response({"details": "not enough money <3"})
