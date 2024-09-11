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

    class Meta:
        verbose_name_plural = 'Links'

    def __str__(self):
        return f"URL: {self.url} Codigo: {self.code}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:
            self.code = Hashids(min_length=4, alphabet='abcdefghijklmnopqrstuvxyz').encode(self.pk)
            self.save()

    def get_absolute_url(self):
        return reverse("core:detail", kwargs={"pk": self.pk})
