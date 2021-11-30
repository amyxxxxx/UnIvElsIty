from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.

class To_do_list(models.Model):
    name=models.CharField(max_length=20)
    body=models.TextField()
    created=models.DateTimeField()
    
    def __str__(self):
        return self.name

