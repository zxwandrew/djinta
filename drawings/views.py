from django.http import HttpResponse
from drawings.models import Drawing
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
#from django.http import Http404

def index(request):
    latest_drawing_list = Drawing.objects.all().order_by('-create_date')[:5]
    return render_to_response(
                              'drawings/index.html', {'latest_drawing_list': latest_drawing_list}
                              )

def detail(request, drawing_id):
    d = get_object_or_404(Drawing, pk=drawing_id)
    return render_to_response(
                              'drawings/detail.html', {'drawing': d}
                              )
    
    
    
    '''try:
        d=Drawing.objects.get(pk=drawing_id)
    except Drawing.DoesNotExist:
        raise Http404
    return render_to_response(
                              'drawings/detail.html', {'drawing': d}
                              )



def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p})'''
    
        
    
    #output = ', '.join([p.drawingpart for p in latest_drawing_list])
    #t= loader.get_template('drawings/index.html')
    #c= Context({
    #       'latest_drawing_list': latest_drawing_list,
    #      })    
    #return HttpResponse(t.render(c))