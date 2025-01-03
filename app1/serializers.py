from rest_framework import serializers
from .models import Messages
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model



class MessageSerializer(serializers.ModelSerializer):

    sender_name = serializers.SlugRelatedField(many=False, slug_field='username', queryset=get_user_model().objects.all())
    receiver_name = serializers.SlugRelatedField(many=False, slug_field='username', queryset=get_user_model().objects.all())

    class Meta:
        model = Messages
        fields = ['sender_name', 'receiver_name', 'description', 'time']
