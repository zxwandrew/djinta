from django.db import models

class Drawing(models.Model):
    drawingpart = models.TextField()
    create_date = models.DateTimeField('date created')