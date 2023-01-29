from ...models import Orders, Withdraw
from rest_framework import serializers


class ListCreateDeleteOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = [
            "amount",
            "price",
            "currency",
            "description",
            "order_type",
            "status",
            
        ]
class WithdrawSerializer(serializers.ModelSerializer):

    class Meta:
        model = Withdraw
        fields = [
        "user",
        "amount",
        "description",
        ]
