from django.db import models

# Create your models here.
class Newslinks(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    date = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    summary = models.CharField(max_length=500, blank=True, null=True)
    text = models.CharField(max_length=10000, blank=True, null=True)
    keywords = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'newslinks'

    def __str__(self):
        return self.title
