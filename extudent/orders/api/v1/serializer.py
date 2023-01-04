from ...models import Orders
from rest_framework import serializers


class ListCreateDeleteOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = [
            "owner",
            "amount",
            "price",
            "currency",
            "description",
            "status",
            
        ]