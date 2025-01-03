# myapp/tasks.py
from celery import shared_task
import time

import requests

import json

from .models import UserRelation, Messages
from app1.serializers import MessageSerializer
from app1.util.AIchatbot import AIchat, llm
from app1.util.SDrequest import main

from stable_diffusion.gen_imgs import gen_3d_person_img_sdxl, gen_2d_img_yden, gen_3d_person_img_sdv1, easy_controlnet_args
from stable_diffusion.find_sd_models import listup_sd_models
from stable_diffusion.custom_hash import hash_checkpoints

#hash_checkpoints()
listup_sd_models()

from django.db import models
from django.contrib.auth import get_user_model

from django.middleware.csrf import get_token

with open('stable_diffusion/data/prompts/base_prompt.json', 'r') as f:
	base_prompt_js = json.load(f)

def send_message(sender_name, receiver_name, message='test'):
	data = {
		'sender_name':sender_name, 
		'receiver_name':receiver_name, 
		'description':message
	}
	serializer = MessageSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		print("done")
	else:
		print(f'serializer is not valid sender:{sender_name} receiver:{receiver_name}')

@shared_task
def background_task():
	base_promt_person_3d_sdxl = base_prompt_js['person']['3d_sdxl']
	base_promt_person_2d = base_prompt_js['person']['2d']
	path_person_3d = "test_sdxl.png"
	path_person_2d = "test_2d.png"
	gen_3d_person_img_sdv1(
		prompt=base_promt_person_3d_sdxl, 
		filename=path_person_3d
		)
	gen_2d_img_yden(
		prompt=base_promt_person_2d, 
		filename=path_person_2d, 
		controlnet_args=easy_controlnet_args(input_image=path_person_3d, control_type="normal", control_weight=0.5)
		)
	logs = []
	i = 0
	#while True:
	#	testuser = get_user_model().objects.filter(is_AI=True)
	#	
	#	
	#	for sender in testuser:
	#		if not sender.username.replace(' ',''):
	#			continue
	#		for receiver in testuser:
	#			if not receiver.username.replace(' ',''):
	#				continue
	#			if sender==receiver:
	#				continue
	#			#messages = Messages.objects.filter(
	#			#    sender_name=sender, receiver_name=receiver
	#			#    ) | Messages.objects.filter(sender_name=sender, receiver_name=receiver)
	#			#log = [message.description for message in messages]
	#			log = '\n'.join(logs)
	#			#new_message = AIchat(sender=sender, receiver=receiver, log=log)
	#			new_message = f'{i}'
	#			send_message(sender_name=sender.username, 
	#						 receiver_name=receiver.username,
	#						 message=new_message
	#						 )
	#			logs.append(new_message)