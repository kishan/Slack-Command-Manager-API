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


@csrf_exempt
def tableflip(request):
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
	

	def sendQuickMessage(text, attachments=[], response_type="in_channel"):
		response = {}
		response["response_type"] = response_type
		response["text"] = text
		attachments = [
					{
						# "text":"Partly cloudy today and tomorrow",
						# "color": "#FF0000",
					}
				]
		response["attachments"] = attachments
		final = response
		return JsonResponse(final)


	def flip(s):
		pchars = u"abcdefghijklmnopqrstuvwxyz,.?!'()[]{}"
		fchars = u"ɐqɔpǝɟƃɥıɾʞlɯuodbɹsʇnʌʍxʎz'˙¿¡,)(][}{"
		flipper = dict(zip(pchars, fchars))
		charList = [ flipper.get(x, x) for x in s.lower() ]
		charList.reverse()
		return "".join(charList)
	
	def table_flipper(text):
		final_text = ""
		if text == "":
			final_text = u'(╯°□°）╯︵ ┻━┻'
		else:
			final_text = u'(╯°□°）╯︵ ' + flip(text)

		if text == "putback":
			final_text = u'┬─┬ノ( º _ ºノ)'

		if text == "mayank":
			final_text = 'Mayank isn\'t even worth the effort of flipping over!!!'
		return final_text

	data = request.POST["text"]
	text_to_send = table_flipper(data)
	return sendQuickMessage(text_to_send)

	