import random
import django
import datetime
import sys
import re
#some extra stuff to help with importing
import os
os.environ['HOME'] = '/tmp'

#import matplotlib
#matplotlib.use('Agg') 

#actual import
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure
#from matplotlib.dates import DateFormatter
#from scipy import *
#from numpy import *
from sympy import *
from django.utils import simplejson
from decimal import Decimal

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
        self.x1=float(min(x1t,x2t))
        self.y1=float(min(y1t, y2t))
        self.x2=float(max(x2t, x1t))
        self.y2=float(max(y2t, y1t))
        self.i=float(it)
        self.e=float(et)
        self.area=float(areat)
        self.length = sqrt(abs(self.x1-self.x2)**2+abs(self.y1-self.y2)**2)
    
    def addjoint (self, jointt, x1t, y1t):
        if(self.x1==x1t and self.y1==y1t):
            self.joint1={'type': jointt}
        elif(self.x2==x1t and self.y2==y1t):
            self.joint2={'type': jointt}
        #ignoring mid member joints for now

class joint:
    def __init__(self, x1t, y1t, typet):
        self.x1=float(x1t)
        self.y1=float(y1t)
        self.type=typet
        
class support:
    magx=None
    magy=None
    def __init__(self, x1t, y1t, typet):
        self.x1=float(x1t)
        self.y1=float(y1t)
        self.type=typet
        
class force:
    def __init__(self, x1t, y1t, typet, magnitudet):
        self.x1=float(x1t)
        self.y1=float(y1t)
        self.type=typet
        self.magnitude = float(magnitudet)
    def getx1(self):
        return self.x1
    def gettype(self):
        return self.type
    def gety1(self):
        return self.y1
    def getmagnitude(self):
        return self.magnitude

def FindReaction(AllParts, AllMembers, AllJoints, AllSupports, AllForces):
    startx=AllSupports[0].x1
    starty=AllSupports[0].y1
    ZMoment=[]
    YMoment=[]
    TempZMoment=[]
    TempYMoment=[]
    SumX=[]
    SumY=[]
    
    unknownx=[]
    unknowny=[]
    xcount=0
    ycount=0
    jointcount=1
    #initiate z and y moment
    
    tempZM=0
    tempYM=0
    tempSumX=0
    tempSumY=0
    
    
    for force in AllForces:
        if(force.gettype()=='XForce'):
            tempYM+=(force.gety1()-starty)*force.getmagnitude()
            tempSumX+=force.getmagnitude()
        if(force.gettype()=='YForce'):
            tempZM+=(force.getx1()-startx)*force.getmagnitude()
            tempSumY+=force.getmagnitude()
        if(force.gettype()=='MForce'):
            tempZM+=force.magnitude()
    
    #Calc X forces from support
    #print(AllSupports)
    for support in AllSupports:
        if (support.magx==None and support.type!='YSupport'):
            tempname='x'+str(xcount)
            unknownx.append(Symbol(tempname))
            
            SumX.append(1)
            TempYMoment.append(support.y1-starty)
            xcount+=1
        #Calc y forces from support
        if (support.magy==None and support.type!='XSupport'):
            tempname='y'+str(ycount)
            unknowny.append(Symbol(tempname))
            
            SumY.append(1)
            TempZMoment.append(support.x1-startx)
            ycount+=1
    
    TempYMoment.append((-1*tempYM))
    TempZMoment.append((-1*tempZM))
    SumX.append(-1*tempSumX)
    SumY.append(-1*tempSumY)
    
    ZMoment.append(TempZMoment)
    ZMoment.append(SumY)
    
    YMoment.append(TempYMoment)
    YMoment.append(SumX)
    
     
    for joint in AllJoints:
        tempZM=0
        tempYM=0
        tempZM2=0
        tempYM2=0
        
        tempSumX=0
        tempSumY=0
        TempZMoment=[]
        TempYMoment=[]
        
        TempYMoment2=[]
        TempZMoment2=[]
    
    
        for force in AllForces:
            if(force.gettype()=='XForce'):
                if(force.gety1()>=joint.y1):
                    tempYM+=(force.gety1()-joint.y1)*force.getmagnitude()
                else:
                    tempYM2+=(force.gety1()-joint.y1)*force.getmagnitude()

            if(force.gettype()=='YForce'):
                if(force.getx1()>=joint.x1):
                    tempZM+=(force.getx1()-joint.x1)*force.getmagnitude()
                else:
                    tempZM2+=(force.getx1()-joint.x1)*force.getmagnitude()

            if(force.gettype()=='MForce'):
                if(force.getx1()>=joint.x1):
                    tempZM+=force.magnitude()
                else:
                    tempZM2+=force.magnitude()
        
        #Calc X forces from support
        #print(AllSupports)
        for support in AllSupports:
            if (support.magx==None and support.type!='YSupport'):
                if(support.y1>=joint.y1):
                    TempYMoment.append(support.y1-joint.y1)
                    TempYMoment2.append(0)
                else:
                    TempYMoment2.append(support.y1-joint.y1)
                    TempYMoment.append(0)
                    
                xcount+=1
            #Calc y forces from support
            if (support.magy==None and support.type!='XSupport'):
                if(support.x1>=joint.x1):
                    TempZMoment.append(support.x1-joint.x1)
                    TempZMoment2.append(0)
                else:
                    TempZMoment2.append(support.x1-joint.x1)
                    TempZMoment.append(0)
                    
                ycount+=1
        
        
        
        TempYMoment.append((-1*tempYM))
        TempZMoment.append((-1*tempZM))
        
        TempYMoment2.append((-1*tempYM2))
        TempZMoment2.append((-1*tempZM2))
        
        ZMoment.append(TempZMoment)        
        YMoment.append(TempYMoment)
        ZMoment.append(TempZMoment2)        
        YMoment.append(TempYMoment2)
        
        jointcount+=1

    #put zmoment into matrix format and solve
    systemz = Matrix(ZMoment)
    print(systemz)
    print(unknowny)
    answerx = solve_linear_system(systemz, *unknowny)
    
    #put ymoment into matrix format and solve
    systemy = Matrix(YMoment)
    print(systemy)
    print(unknownx)
    answery = solve_linear_system(systemy, *unknownx)
    
    #return answer
    print(answerx)
    return (answerx)
    
def MainParse(form):
    
    #DPs = simplejson.loads(form)
    AllParts=[]
    AllMembers=[]
    AllJoints=[]
    AllSupports=[]
    AllForces=[]
    ObjNum=0
    
    #Will need to be deleted in the future
    form=[{u'y2': 300, u'e': 300000, u'i': 100, u'area': 10, u'servy1': 25, u'servx1': 5, u'servx2': 10, u'x2': 150, u'servy2': 25, u'y1': 300, u'x1': 75, u'type': u'member'}, {u'y2': 300, u'e': 300000, u'i': 100, u'area': 10, u'servy1': 25, u'servx1': 10, u'servx2': 20, u'x2': 300, u'servy2': 25, u'y1': 300, u'x1': 150, u'type': u'member'}, {u'y1': 300, u'servy1': 25, u'x1': 150, u'type': u'Hinge', u'servx1': 10}, {u'y1': 300, u'servy1': 25, u'x1': 75, u'type': u'YSupport', u'servx1': 5}, {u'y1': 300, u'servy1': 25, u'x1': 300, u'type': u'PinSupport', u'servx1': 20}, {u'y1': 300, u'servy1': 25, u'x1': 225, u'type': u'YSupport', u'servx1': 15}, {u'servy1': 25, u'servx1': 12, u'magnitude': u'-100', u'y1': 180, u'x1': 180, u'type': u'YForce'}]
    
    for x in form:
        print(x['type'])
        if(x['type']=='member'):
            tempmember = member(x['servx1'], x['servy1'], x['servx2'], x['servy2'], x['i'], x['e'], x['area'])
            AllParts.append(tempmember)
            AllMembers.append(tempmember)
        elif(x['type']=='Hinge' or x['type']=='FixedJoint'):
            tempjoint = joint(x['servx1'], x['servy1'], x['type']);
            AllParts.append(tempjoint)
            AllJoints.append(tempjoint)
        elif(x['type']=='XSupport' or x['type']=='YSupport' or x['type']=='PinSupport' or x['type']=='FixedSupport'):
            tempsupport = support(x['servx1'], x['servy1'], x['type']);
            AllParts.append(tempsupport)
            AllSupports.append(tempsupport)
        elif(x['type']=='Xforce' or x['type']=='YForce' or x['type']=='MSupport' or x['type']=='DSupport'):
            tempforce = force(x['servx1'], x['servy1'], x['type'], x['magnitude']);
            AllParts.append(tempforce)
            AllForces.append(tempforce)
        ObjNum+=1
        
    answer=FindReaction(AllParts, AllMembers, AllJoints, AllSupports, AllForces)
    
    #check=42
    #AllParts=[['ihi'],['wsaasdf'],[12]]
    #temp=form[0]['x1']
    print(answer)
    return AllParts

output = MainParse(sys.argv[1])
    




