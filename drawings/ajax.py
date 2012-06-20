from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

from django.http import HttpResponse, HttpResponseRedirect
from drawings.models import Drawing
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.forms.models import modelformset_factory
from django.core.context_processors import csrf
from datetime import date, datetime
from django.utils import simplejson



@dajaxice_register
def myexample(request, drawingpart):
    return simplejson.dumps({'message':'You Sent%s!' % drawingpart})

@dajaxice_register
def send_form(request, form):
    #DP = form.cleaned_data.get('DP')
    DP = simplejson.loads(form)
    d2 = Drawing(drawingpart=DP, create_date=datetime.now())
    d2.save()

    return simplejson.dumps({'message':'You Sent%s!' % DP})