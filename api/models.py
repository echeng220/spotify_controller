'''
Django mindset: Fat models, thin views. Put as much info as you can in the models
'''

import string
import random
from django.db import models

def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break

    return code

class Room(models.Model):
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True) # host can't have multiple rooms 
    guestCanPause = models.BooleanField(null=False, default=False)
    votesToSkip = models.IntegerField(null=False, default=1)
    createdAt = models.DateTimeField(auto_now_add=True)
