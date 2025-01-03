import requests,bs4

from .models import UserRelation, Messages
from app1.util.AIchatbot import AIchat, llm
from app1.util.SDrequest import main
from app1.serializers import MessageSerializer

from django.db import models
from django.contrib.auth import get_user_model

from django.middleware.csrf import get_token

def main():
    testusers = get_user_model().objects.filter(is_AI=True)
    sender = testusers[0]
    receiver = testusers[1]
    data = {
        'sender_name':sender.username, 
        'receiver_name':receiver.username, 
        'description':'test from python'
    }
    serializer = MessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print("done")
    else:
        print('serializer is not valid')