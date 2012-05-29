from django.http import HttpResponse
from drawings.models import Drawing
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.forms.models import modelformset_factory
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

def create(request):
    DrawingFormSet = modelformset_factory(Drawing)
    if request.method=="POST":
        formset = DrawingFormSet(request.Post, request.FILES)
        if formset.is_valid():
            formset.save()
    else:
        formset = DrawingFormSet()
    return render_to_response("drawings/create.html", {"formset": formset,}) 


"""
def manage_authors(request):
    AuthorFormSet = modelformset_factory(Author)
    if request.method == 'POST':
        formset = AuthorFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # do something.
    else:
        formset = AuthorFormSet()
    return render_to_response("manage_authors.html", {
        "formset": formset,
    })
"""
    
    
    
'''
def detail(request, drawing_id):
    try:
        d=Drawing.objects.get(pk=drawing_id)
    except Drawing.DoesNotExist:
        raise Http404
    return render_to_response(
                              'drawings/detail.html', {'drawing': d}
                              )
    '''
    #output = ', '.join([p.drawingpart for p in latest_drawing_list])
    #t= loader.get_template('drawings/index.html')
    #c= Context({
    #       'latest_drawing_list': latest_drawing_list,
    #      })    
    #return HttpResponse(t.render(c))