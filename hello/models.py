from django.db import models

# Create your models here.
class Sentiment(models.Model):
  link     = models.TextField(max_length=200, null=True)
  data     = models.DateField()
  rezultat = models.TextField(max_length=300, null=True)
