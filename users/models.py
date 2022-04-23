from turtle import update
from venv import create
from django.db import models

class User(models.Model):
    username    = models.CharField(max_length=100)
    email       = models.CharField(max_length=100,unique=True)
    password    = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=50)
    created_at  = models.DateField(auto_now_add=True)
    update_at   = models.DateField(auto_now=True)

    class Meta:
        db_table = 'users' 

# Create your models here.
