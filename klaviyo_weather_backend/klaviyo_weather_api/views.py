# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import City
from rest_framework import viewsets
from serializers import UserSerializer,MessageSerializer,CitySerializer
from models import User,City
from datetime import datetime,timedelta
from rest_framework.response import Response
from rest_framework import status
import requests
import json
import pytz
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import render
import smtplib
import requests
import sendgrid
from sendgrid.helpers.mail import *
import base64


# Create your views here.
api_key=settings.API_KEY
condition_url="http://api.wunderground.com/api/" +api_key+ "/conditions/q/"
planner_url="http://api.wunderground.com/api/" +api_key+ "/planner_"

class UserList(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User

    def get_queryset(self):
        #print self.request.user
        return User.objects.all()
        # return UserEventHistory

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            kwargs = serializer.validated_data
            user_data = User(**kwargs)
            print datetime.now(pytz.timezone('America/Phoenix'))
            user_data.creationTime = datetime.now(pytz.timezone('America/Phoenix'))
            global condition_url
            city_data=City.objects.filter(id=self.request.data['cityId'])
            if city_data is not None:
                name=city_data[0].name
                state=city_data[0].state
                request_URL=condition_url+state.replace(" ","_")+"/"+name.replace(" ","_")+".json"
                print request_URL
                request_data=requests.get(request_URL)
                request_json= json.loads(request_data.content)
                user_data.timezone=request_json['current_observation']['local_tz_short']
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user_data.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CityList(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    model = City
    def get_queryset(self):
        return City.objects.all()


class Message(object):
    def __init__(self, city,state,subject, body, icon_url,avg):
        self.city = city
        self.state = state
        self.subject = subject
        self.body = body
        self.icon_url = icon_url
        self.avg = avg

def getMessage(city_data):
    name = city_data[0].name
    state = city_data[0].state
    request_URL = condition_url + state.replace(" ", "_") + "/" + name.replace(" ", "_") + ".json"
    print request_URL
    request_data = requests.get(request_URL)
    request_json = json.loads(request_data.content)
    icon = request_json['current_observation']['icon']
    icon_url = request_json['current_observation']['icon_url']
    weather_now = request_json['current_observation']['temp_f']
    weather_type = request_json['current_observation']['weather']
    local_time = request_json['current_observation']["local_time_rfc822"]
    range1 = datetime.now() + timedelta(-15)
    range2 = datetime.now() + timedelta(15)
    range1_day = range1.day if range1.day >= 10 else "0" + str(range1.day)
    range1_month = range1.month if range1.month >= 10 else "0" + str(range1.month)
    range2_day = range2.day if range2.day >= 10 else "0" + str(range2.day)
    range2_month = range2.month if range2.month >= 10 else "0" + str(range2.month)
    history_url = planner_url + str(range1_month) + str(range1_day) + str(range2_month) \
                  + str(range2_day) + "/q/" + state.replace(" ", "_") + "/" + name.replace(" ", "_") + ".json"
    history_data = requests.get(history_url)
    history_json = json.loads(history_data.content)
    max_avg = float(history_json['trip']['temp_high']['avg']["F"])
    min_avg = float(history_json['trip']['temp_low']['avg']["F"])
    final_avg = (max_avg + min_avg) / 2.0
    print final_avg
    weather_now = float(weather_now)
    msg_subject = ""
    msg_body = ""
    if ((weather_now - final_avg) >= 5 or icon == "sunny"):
        msg_subject = "It's nice out! Enjoy a discount on us."
        msg_body = str(weather_now) + " degree, " + str(weather_type)
    elif (weather_now - final_avg) <= -5 or icon == "cloudy":
        msg_subject = "Not so nice out? That's okay, enjoy a discount on us."
        msg_body = str(weather_now) + " degree, " + str(weather_type)
    else:
        msg_subject = "Enjoy a discount on us."
        msg_body = str(weather_now) + " degree, " + str(weather_type)
    message = Message(name, state, subject=msg_subject, body=msg_body, icon_url=icon_url, avg=final_avg)
    return message

def sendEmail(to,message):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SEND_GRID_KEY)
    from_email = Email("klaviyo@example.com")
    to_email = Email(to)
    subject = message.subject
    content = Content("text/html", "<h1>Location: "+message.city+", "+message.state+"</h1><h1>"+message.body+"</h1>")
    mail = Mail(from_email, subject, to_email, content)
    attachment = Attachment()
    response_image = requests.get(message.icon_url)
    attachment.content=base64.b64encode(response_image.content)
    attachment.type="image/png"
    attachment.filename = "banner.png"
    attachment.content_id = "Banner"
    mail.add_attachment(attachment)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


class UserMessage(APIView):

    def get(self, request, format=None):
        global condition_url,planner_url
        city_id = self.request.query_params.get('cityId', None)
        if city_id is not None:
            city_data = City.objects.filter(id=city_id)
            if city_data is not None:
                message=getMessage(city_data)
                serializer=MessageSerializer(message)
                return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return_data={}
            return_data['cityId']=["cityId is required"]
            return Response(return_data,status=status.HTTP_400_BAD_REQUEST)

class EmailAPI(APIView):
    def post(self, request, format=None):
        timez=None
        if "timezone" in self.request.data:
            timez=self.request.data['timezone']
        if timez is None:
            users = User.objects.all()
            return_data = {}
            for user in users:
                print user
                city_data = City.objects.filter(id=user.cityId.id)
                message = getMessage(city_data)
                try:
                    sendEmail(user.email, message)
                    return_data[user.email] = "Success"
                except Exception as inst:
                    print inst
                    return_data[user.email] = "Failure"

            return Response(return_data, status=status.HTTP_200_OK)
        else:
            users = User.objects.filter(timezone=timez)
            return_data = {}
            if users is None:
                return Response(return_data, status=status.HTTP_400_BAD_REQUEST)
            for user in users:
                print user
                city_data = City.objects.filter(id=user.cityId.id)
                message = getMessage(city_data)
                try:
                    sendEmail(user.email, message)
                    return_data[user.email] = "Success"
                except Exception as inst:
                    print inst
                    return_data[user.email] = "Failure"
            return Response(return_data, status=status.HTTP_200_OK)