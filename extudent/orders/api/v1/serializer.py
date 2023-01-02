from ...models import Orders
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Orders
        fields = [
            "amount",
            "price",
            "owner",
            "buyer",
            "currency",
            "description",
            "status",
            
        ]