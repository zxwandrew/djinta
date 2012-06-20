import random
import django
import datetime
#some extra stuff to help with importing
import os
os.environ['HOME'] = '/tmp'
import matplotlib
matplotlib.use('Agg') 
#actual import
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from scipy import *
from numpy import *
from sympy import *
from django.utils import simplejson

# file charts.py, a stupid little test to see if plot was working
def simple(request):
    fig = Figure()
    ax = fig.add_subplot(111)
    x = []
    y = []
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now += delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

class member:
    def __init__(self, x1t, y1t, x2t, y2t, it, et, areat):
        self.x1=min(x1t,x2t)
        self.y1=min(y1t, y2t)
        self.x2=max(x2t, x1t)
        self.y2=max(y2t, y1t)
        self.i=it
        self.e=et
        self.area=areat
        self.length = sqrt(abs(self.x1-self.x2)^2+abs(self.y1-self.y2)^2)
    
    def addjoint (self, jointt, x1t, y1t):
        if(self.x1==x1t and self.y1==y1t):
            self.joint1={'type': jointt}
        elif(self.x2==x1t and self.y2==y1t):
            self.joint2={'type': jointt}
        #ignoring mid member joints for now

class joint:
    def __init__(self, x1t, y1t, typet):
        self.x1=x1t
        self.y1=y1t
        self.type=typet
class support:
    magx=None
    magy=None
    def __init__(self, x1t, y1t, typet):
        self.x1=x1t
        self.y1=y1t
        self.type=typet
class force:
    def __init__(self, x1t, y1t, typet, magnitudet):
        self.x1=x1t
        self.y1=y1t
        self.type=typet
        self.magnitude = magnitudet
    def getx1(self):
        return self.x1
    def gettype(self):
        return self.type
    def gety1(self):
        return self.y1
    def getmagnitude(self):
        return self.magnitude

def FindReaction(AllParts, AllMembers, AllJoints, AllSupports, AllForces):
    startx=AllJoints[0]['x1']
    starty=AllJoints[1]['y1']
    ZMoment=0
    YMoment=0
    xcount=0
    ycount=0
    for force in AllForces:
        if(force.gettype()=='YForce'):
            ZMoment+=(force.getx1()-startx)*force.magnitude()
        if(force.gettype()=='XForce'):
            YMoment+=(force.gety1()-starty)*force.magnitude()
        if(force.gettype()=='MForce'):
            ZMoment+=force.magnitude()
    #Calc X forces from support
    for support in AllSupports:
        if (support.magx==None and support.type!='YSupport'):
            tempname='x'+str(xcount)
            x=Symbol(tempname)
            YMoment+=(support.getx1()-startx)*x
            xcount+=1
        #Calc y forces from support
        if (support.magy==None and support.type!='XSupport'):
            tempname='y'+str(ycount)
            y=Symbol(tempname)
            ZMoment+=(support.getx1()-startx)*y
            ycount+=1
        answer=solve([ZMoment])
        return answer['x1']
    
def MainParse(form):
    '''
    DPs = simplejson.loads(form)
    AllParts=[]
    AllMembers=[]
    AllJoints=[]
    AllSupports=[]
    AllForces=[]
    ObjNum=0
    for x in DPs:
        if(x['type']=='member'):
            tempmember = member(x['servx1'], x['servy1'], x['servx2'], x['servy2'], x['i'], x['e'], x['area'])
            AllParts.append(tempmember)
            AllMembers.append(tempmember)
        elif(x['type']=='Hinge' or x['type']=='FixedJoint'):
            tempjoint = joint(x['servx1'], x['servy1'], x['type']);
            AllParts.append(tempjoint)
            AllJoints.append(tempjoint)
        elif(x['type']=='XSupport' or x['type']=='YSupport' or x['type']=='PinSupport' or x['type']=='FixedSupport'):
            tempsupport = joint(x['servx1'], x['servy1'], x['type']);
            AllParts.append(tempsupport)
            AllSupports.append(tempsupport)
        elif(x['type']=='Xforce' or x['type']=='YForce' or x['type']=='MSupport' or x['type']=='DSupport'):
            tempforce = joint(x['servx1'], x['servy1'], x['type'], x['magnitude']);
            AllParts.append(tempforce)
            AllForces.append(tempforce)
        ObjNum+=1
        '''
    #answer=FindReaction(AllParts, AllMembers, AllJoints, AllSupports, AllForces)
    
    check=42
    return check
    




