from ...models import Message
from rest_framework.serializers import ModelSerializer


class MessageSerializer(ModelSerializer):
    
    class Meta:
        model = Message
        fields = [
            "writer",
            "reciver",
            "title",
            "text",
            "attached_pic",
            "is_recived",
        ]