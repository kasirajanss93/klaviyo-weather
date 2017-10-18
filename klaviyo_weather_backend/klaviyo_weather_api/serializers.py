from rest_framework import serializers
from models import User,City


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'cityId')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name','state')


class MessageSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=200)
    state = serializers.CharField(max_length=200)
    subject = serializers.CharField(max_length=200)
    body = serializers.CharField(max_length=200)
    icon_url = serializers.CharField(max_length=200)
    avg=serializers.CharField(max_length=200)