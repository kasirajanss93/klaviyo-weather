# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class City(models.Model):
    id=models.IntegerField(primary_key=True)
    name = models.TextField()
    state = models.TextField()
    population = models.IntegerField()
    growth = models.TextField()

class User(models.Model):
    email=models.EmailField(primary_key=True)
    cityId=models.ForeignKey(City,on_delete=models.CASCADE)
    timezone=models.TextField()
    creationTime=models.DateTimeField()
