from django.forms import ModelForm
from drawings.models import Drawing

class DrawingForm(ModelForm):
    class Meta:
        model = Drawing
        fields = ('drawingpart')