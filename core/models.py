from django.db import models
from django.urls import reverse
from hashids import Hashids
import datetime


# Create your models here.
class Link(models.Model):
    url = models.URLField()
    code = models.CharField(max_length=8, blank=True)
    date = models.DateField(auto_now_add=True)
    count = models.PositiveIntegerField(default=0)