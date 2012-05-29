from django.db import models
from django.forms import ModelForm

class Drawing(models.Model):
    drawingpart = models.TextField()
    create_date = models.DateTimeField('date created')
