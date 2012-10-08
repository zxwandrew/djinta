from dajaxice.decorators import dajaxice_register

from django.http import HttpResponse, HttpResponseRedirect
from drawings.models import Drawing
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.forms.models import modelformset_factory
from django.core.context_processors import csrf
from datetime import date, datetime
from django.utils import simplejson
from drawings.calc import *



@dajaxice_register
def myexample(request, drawingpart):
    return simplejson.dumps({'message':'You Sent%s!' % drawingpart})

@dajaxice_register
def send_form(request, form):
    #DP = form.cleaned_data.get('DP')
    #temp = [{"type":"member","x1":88,"y1":105,"x2":205,"y2":235,"servx1":"5.867","servy1":"18.000","servx2":"13.667","servy2":"9.333","e":300000,"i":100,"area":10},{"type":"member","x1":205,"y1":235,"x2":311,"y2":175,"servx1":"13.667","servy1":"9.333","servx2":"20.733","servy2":"13.333","e":300000,"i":100,"area":10},{"type":"member","x1":311,"y1":175,"x2":431,"y2":283,"servx1":"20.733","servy1":"13.333","servx2":"28.733","servy2":"6.1"}]
    DP = simplejson.loads(form)
    temp = MainParse(DP)
    #DP=[{"type":"member","e":300000,"i":100,"area":10}]
    #d2 = Drawing(drawingpart=DP, create_date=datetime.now())
    #d2.save()

    return simplejson.dumps(AllJson))
    #return temp