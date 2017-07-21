# -*- coding: utf-8 -*- 

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt
import os
import requests
import json


@csrf_exempt
def index(request):
	return HttpResponse("Hello World")


def request_check(request):
	if request.method != "POST":
			return HttpResponseBadRequest("400 Request should be of type POST.")

	if settings.VERIFY_COMMANDS:
		verification_token = os.environ.get("TABLEFLIP_TOKEN", "not here")
		try:
			sent_token = request.POST["token"]
		except KeyError:
			return HttpResponseBadRequest("400 Request is not signed!")
		else:
			if verification_token != sent_token:
				print verification_token + " __ " + sent_token
				return HttpResponseBadRequest("400 Request not signed with correct token!")
	return True



def sendQuickMessage(text, attachments=[], response_type="in_channel"):
	response = {}
	response["response_type"] = response_type
	response["text"] = text
	if (len(text) > 1): 
		first_letter = text[1]
	else:
		first_letter ="a"
	if ((len(text) > 0) and (text[0] != "#")):
		response['text'] = ":warning: Please enter in valid channel (#channel_name)"
		return JsonResponse(response)
	sent_map = {'a': 0.233, 'c': 0.053, 'b': 0.004, 'e': 0.005, 'd': 0.023, 'g': 0.147, 'f': 0.246, 'i': -0.232, 'h': 0.062, 'k': 0.095, 'j': 0.137, 'm': 0.061, 'l': 0.051, 'o': 0.198, 'n': 0.222, 'q': 0.164, 'p': 0.188, 's': 0.163, 'r': 0.22, 'u': 0.153, 't': 0.052, 'w': 0.108, 'v': 0.168, 'y': 0.089, 'x': 0.144, 'z': 0.024}
	sent_score = sent_map[first_letter]
	if sent_score > 0:
		color = "#21CA23"
	else:
		color = "#FF0000"
	attachments = [
				{
					"text":"Sentiment Score: " + str(sent_score),
					"color": color,
				}
			]
	response["attachments"] = attachments

	final = response
	# final = {
	#     "text": "Select the channel you want to see the sentiment of",
	#     "response_type": "in_channel",
	#     "attachments": [
	#         {
	#             "fallback": "Upgrade your Slack client to use messages like these.",
	#             "color": "#3AA3E3",
	#             "attachment_type": "default",
	#             "callback_id": "select_simple_1234",
	#             "actions": [
	#                 {
	#                     "name": "channels_list",
	#                     "text": "Select channel",
	#                     "type": "select",
	#                     "data_source": "channels"
	#                 }
	#             ]
	#         }
	#     ]
	# }
	return JsonResponse(final)



@csrf_exempt
def sentiment(request):
	ret = request_check(request)
	if (ret != True): return ret
	
	data = request.POST["text"]
	text_to_send = data
	return sendQuickMessage(text_to_send)


@csrf_exempt
def sentiment_channel(request):
	ret = request_check(request)
	if (ret != True): return ret

	import pprint
	pp = pprint.PrettyPrinter(indent=4)

	
	# TODO: get channel and response url from request
	print request.POST['payload']
	text_to_send = "AAAA"


	response = {}
	response["response_type"] = "in_channel"
	response["text"] = text_to_send
	attachments = [
				{
					"text":"Partly cloudy today and tomorrow",
					"color": "#FF0000",
				}
			]
	response["attachments"] = attachments
	return JsonResponse(response)
	return sendQuickMessage(text_to_send)

















