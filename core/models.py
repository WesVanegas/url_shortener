from django.db import models
from django.urls import reverse
from hashids import Hashids
import datetime


# Create your models here.
class LinkQuerySet(models.QuerySet):
    def decode_enlace(self, code):
        decode = Hashids(min_length=4, alphabet='abcdefghijklmnopqrstuvxyz').decode(code)[0]
        self.filter(pk=decode).update(count=models.F('count') + 1)
        return self.filter(pk=decode).first().url

    def total_links(self):
        return self.count()

    def total_redirections(self):
        return self.aggregate(redirecciones=models.Sum('count'))

    def dates(self, pk):
        return self.values('date').annotate(
            september = models.Sum('count', filter=models.Q(filter__gte=datetime.date(2024, 9, 1), filter__lte=datetime.date(2024, 9, 30)))
        ).filter(pk=pk)


class Link(models.Model):
    url = models.URLField()
    code = models.CharField(max_length=8, blank=True)
    date = models.DateField(auto_now_add=True)
    count = models.PositiveIntegerField(default=0)

    links = LinkQuerySet.as_manager()

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
