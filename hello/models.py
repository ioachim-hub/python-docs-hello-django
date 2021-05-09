from django.db import models

# Create your models here.
class Sentiment(models.Model):
  link     = model.TextField(max_length=200, null=True)
  data     = model.DateField()
  rezultat = model.TextField(max_length=300, null=True)
