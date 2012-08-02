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
import math
from django.utils import simplejson
from decimal import Decimal
from operator import itemgetter, attrgetter

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
    def __init__(self, x1t, y1t, x2t, y2t, it, et, areat,namet):
        self.x1=float(min(x1t,x2t))
        self.y1=float(min(y1t, y2t))
        self.x2=float(max(x2t, x1t))
        self.y2=float(max(y2t, y1t))
        self.i=float(it)
        self.e=float(et)
        self.area=float(areat)
        self.length = sqrt(abs(self.x1-self.x2)**2+abs(self.y1-self.y2)**2)
        self.name=namet
    
    def addjoint (self, jointt, x1t, y1t):
        if(self.x1==x1t and self.y1==y1t):
            self.joint1={'type': jointt}
        elif(self.x2==x1t and self.y2==y1t):
            self.joint2={'type': jointt}
        #ignoring mid member joints for now

class joint:
    def __init__(self, x1t, y1t, typet,namet):
        self.x1=float(x1t)
        self.y1=float(y1t)
        self.type=typet
        self.name=namet
        
class support:
    magx=None
    magy=None
    def __init__(self, x1t, y1t, typet,namet):
        self.x1=float(x1t)
        self.y1=float(y1t)
        self.type=typet
        self.name=namet
        
        
class force:
    def __init__(self, x1t, y1t, typet, magnitudet,namet):
        self.x1=float(x1t)
        self.y1=float(y1t)
        self.type=typet
        self.magnitude = float(magnitudet)
        self.name=namet
    def getx1(self):
        return self.x1
    def gettype(self):
        return self.type
    def gety1(self):
        return self.y1
    def getmagnitude(self):
        return self.magnitude

class dforce:
    def __init__(self, x1t, y1t, x2t,y2t, typet, f1t, f2t, directiont, onmembert, r1t, r2t, slopet, namet):
        self.x1=float(x1t)
        self.y1=float(y1t)
        self.x2=float(x2t)
        self.y2=float(y2t)
        self.type=typet
        self.f1 = float(f1t)
        self.f2 = float(f2t)
        self.r1= float(r1t)
        self.r2= float(r2t)
        self.direction = directiont
        self.onmember=onmembert
        self.slope=slopet
        self.name=namet
    def gettype(self):
        return self.type

def FindReaction(AllParts, AllMembers, AllJoints, AllSupports, AllForces):
    startx=AllSupports[0].x1
    starty=AllSupports[0].y1
    ZMoment=[]
    YMoment=[]
    
    TempZMoment=0
    TempYMoment=0
    SumX=0
    SumY=0
    
    unknownx=[]
    unknowny=[]
    unknown=[]
    xcount=0
    ycount=0
    mcount=0
    allcount=0
    jointcount=1

    
    for force in AllForces:
        if(force.gettype()=='XForce'):
            TempZMoment+=(force.gety1()-starty)*force.getmagnitude()
            SumX+=force.getmagnitude()
        if(force.gettype()=='YForce'):
            TempZMoment+=(force.getx1()-startx)*force.getmagnitude()
            SumY+=force.getmagnitude()
        if(force.gettype()=='MForce'):
            TempZMoment+=force.magnitude()
        if(force.gettype()=='DForce'):
            if(force.direction=="Global-Y"):
                print(force.x1)
                print(force.x2)
                print((((force.x2-force.x1)/2+force.x1)-startx))
                TempZMoment+=(((force.x2-force.x1)/2+force.x1)-startx)*((force.f1+force.f2)*(force.r2-force.r1)/2)
                SumY+=(force.f1+force.f2)*(force.r2-force.r1)/2
            elif(force.direction=="Local-Y"):
                angle = math.atan(slope)
                f1x = f1*math.sin(angle)
                f1y = f1*math.cos(angle)
                f2x = f2*math.sin(angle)
                f2y = f2*math.cos(angle)
                
                TempZMoment+=((force.y1+((force.y2-force.y1)*(2*f1x+f2x)/(3*(f1x+f2x)))-starty)*((f1x+f2x)*(force.r2-force.r1)/2))
                TempZMoment+=((force.x1+((force.x2-force.x1)*(2*f1y+f2y)/(3*(f1y+f2y)))-startx)*((f1y+f2y)*(force.r2-force.r1)/2))
                SumX+=(force.f1x+force.f2x)*(force.r2-force.r1)/2
                SumY+=(force.f1y+force.f2y)*(force.r2-force.r1)/2
                
                
            elif(force.direction=="Global-X"):
                TempZMoment+=((force.y2-force.y1)/2-starty)*((force.f1+force.f2)*(force.r2-force.r1)/2)
                SumX+=(force.f1+force.f2)*(force.r2-force.r1)/2
            elif(force.direction=="Local-X"):
                angle = math.atan(slope)
                f1x = f1*math.sin(angle)
                f1y = f1*math.cos(angle)
                f2x = f2*math.sin(angle)
                f2y = f2*math.cos(angle)
                
                TempZMoment+=((force.y1+((force.y2-force.y1)*(2*f1x+f2x)/(3*(f1x+f2x)))-starty)*((f1x+f2x)*(force.r2-force.r1)/2))
                TempZMoment+=((force.x1+((force.x2-force.x1)*(2*f1y+f2y)/(3*(f1y+f2y)))-startx)*((f1y+f2y)*(force.r2-force.r1)/2))
                SumX+=(force.f1x+force.f2x)*(force.r2-force.r1)/2
                SumY+=(force.f1y+force.f2y)*(force.r2-force.r1)/2
                
    
    #Calc X forces from support
    #print(AllSupports)
    for support in AllSupports:
        if (support.magx==None and support.type!='YSupport'):
            tempname='x'+str(xcount)
            x=Symbol(tempname)
            unknownx.append(x)
            unknown.append(x)
            
            SumX+=x
            TempZMoment+=(support.y1-starty)*x
            xcount+=1
            allcount+=1
        #Calc y forces from support
        if (support.magy==None and support.type!='XSupport'):
            tempname='y'+str(ycount)
            y=Symbol(tempname)
            unknowny.append(y)
            unknown.append(y)
            
            SumY+=y
            TempZMoment+=(support.x1-startx)*y
            ycount+=1
            allcount+=1
        #Calc m forces
        if (support.type=='FixedSupport'):
            tempname='m'+str(mcount)
            m=Symbol(tempname)
            unknown.append(m)
            unknowny.append(m)
            
            TempZMoment+=m
            SumY+=0*m
            mcount+=1
            allcount+=1
       
    ZMoment.append(TempZMoment)
    ZMoment.append(SumY)
    #YMoment.append(TempYMoment)
    YMoment.append(SumX)
    
    print(ZMoment)
    
     
    for joint in AllJoints:
        TempZMoment=0
        TempYMoment=0
        
        TempZMoment2=0
        TempYMoment2=0
        
        xcount=0
        ycount=0
        allcount=0
    
    
        for force in AllForces:
            if(force.gettype()=='XForce'):
                if(force.gety1()>=joint.y1):
                    TempZMoment+=(force.gety1()-joint.y1)*force.getmagnitude()
                else:
                    #TempZMoment2+=(force.gety1()-joint.y1)*force.getmagnitude()
                    TempZMoment+=(force.gety1()-joint.y1)*force.getmagnitude()

            if(force.gettype()=='YForce'):
                if(force.getx1()>=joint.x1):
                    TempZMoment+=(force.getx1()-joint.x1)*force.getmagnitude()
                else:
                    #TempZMoment2+=(force.getx1()-joint.x1)*force.getmagnitude()
                    TempZMoment+=(force.getx1()-joint.x1)*force.getmagnitude()

            if(force.gettype()=='MForce'):
                if(force.getx1()>=joint.x1):
                    TempZMoment+=force.magnitude()
                else:
                    #TempZMoment2+=force.magnitude()
                    TempZMoment+=force.magnitude()
            if(force.gettype()=='DForce'):
                if(force.direction=="Global-Y"):
                    TempZMoment+=((force.x2-force.x1)/2-startx)*((force.f1+force.f2)*(force.r2-force.r1)/2)
                    SumY+=(force.f1+force.f2)*(force.r2-force.r1)/2
                elif(force.direction=="Local-Y"):
                    angle = math.atan(slope)
                    f1x = f1*math.sin(angle)
                    f1y = f1*math.cos(angle)
                    f2x = f2*math.sin(angle)
                    f2y = f2*math.cos(angle)
                    
                    TempZMoment+=((force.y1+((force.y2-force.y1)*(2*f1x+f2x)/(3*(f1x+f2x)))-starty)*((f1x+f2x)*(force.r2-force.r1)/2))
                    TempZMoment+=((force.x1+((force.x2-force.x1)*(2*f1y+f2y)/(3*(f1y+f2y)))-startx)*((f1y+f2y)*(force.r2-force.r1)/2))
                    SumX+=(force.f1x+force.f2x)*(force.r2-force.r1)/2
                    SumY+=(force.f1y+force.f2y)*(force.r2-force.r1)/2
                    
                    
                elif(force.direction=="Global-X"):
                    TempZMoment+=((force.y2-force.y1)/2-starty)*((force.f1+force.f2)*(force.r2-force.r1)/2)
                    SumX+=(force.f1+force.f2)*(force.r2-force.r1)/2
                elif(force.direction=="Local-X"):
                    angle = math.atan(slope)
                    f1x = f1*math.sin(angle)
                    f1y = f1*math.cos(angle)
                    f2x = f2*math.sin(angle)
                    f2y = f2*math.cos(angle)
                    
                    TempZMoment+=((force.y1+((force.y2-force.y1)*(2*f1x+f2x)/(3*(f1x+f2x)))-starty)*((f1x+f2x)*(force.r2-force.r1)/2))
                    TempZMoment+=((force.x1+((force.x2-force.x1)*(2*f1y+f2y)/(3*(f1y+f2y)))-startx)*((f1y+f2y)*(force.r2-force.r1)/2))
                    SumX+=(force.f1x+force.f2x)*(force.r2-force.r1)/2
                    SumY+=(force.f1y+force.f2y)*(force.r2-force.r1)/2
                    
                    #force.y1+((force.y2-force.y1)*(2*force.f1x+force.f2x)/(3*(force.f1x+force.f2x)))
                    
                    #force.x1+((force.x2-force.x1)*(2*force.f1y+force.f2y)/(3*(force.f1y+force.f2y)))
            
        
        #Calc X forces from support
        #print(AllSupports)
        for support in AllSupports:
            if (support.magx==None and support.type!='YSupport'):
                if(support.y1>=joint.y1):
                    TempZMoment+=(support.y1-joint.y1)*unknown[allcount]
                else:
                    #TempZMoment2+=(support.y1-joint.y1)*unknown[allcount]
                    TempZMoment+=(support.y1-joint.y1)*unknown[allcount]
                    
                xcount+=1
                allcount+=1
                
            #Calc y forces from support
            if (support.magy==None and support.type!='XSupport'):
                if(support.x1>=joint.x1):
                    TempZMoment+=(support.x1-joint.x1)*unknown[allcount]
                else:
                    #TempZMoment2+=(support.x1-joint.x1)*unknown[allcount]
                    TempZMoment+=(support.x1-joint.x1)*unknown[allcount]
                    
                ycount+=1
                allcount+=1
            if(support.type=='FixedSupport'):
                TempZMoment+=unknown[allcount]
                mcount+=1
                allcount+=1
                

        
        ZMoment.append(TempZMoment)        
        #YMoment.append(TempYMoment)
        ZMoment.append(TempZMoment2)        
        #YMoment.append(TempYMoment2)
        
        jointcount+=1
   
   
    #put zmoment into matrix format and solve
    #mat1=Matrix(((0,15.0,10.0,700.0),(1,1,1,100),(0,10.0,5.0,200.0),(-5.0,0,0,0)))
    systemz = set(ZMoment)
    print(systemz)    
    print(unknowny)
    answery = solve(systemz, *unknowny)
    
    #put ymoment into matrix format and solve
    systemy = set(YMoment)
    print(systemy)
    print(unknownx)
    answerx = solve(systemy, *unknownx)
    
    #return answer
    print(answery)
    print(answerx)

    xcount=0
    ycount=0
    scount=0
    answer={}
    for support in AllSupports:
        if (support.magx==None and support.type!='YSupport'):
            support.magx=answerx[unknownx[xcount]]
            answer[str(scount)+'x']=answerx[unknownx[xcount]]
            xcount+=1
        
        if (support.magy==None and support.type!='XSupport'):    
            support.magy=answery[unknowny[ycount]]
            answer[str(scount)+'y']=answery[unknowny[ycount]]
            ycount+=1
        scount+=1
            
    return (answer)

    
def MainParse(form):
    
    #DPs = simplejson.loads(form)
    AllParts=[]
    AllMembers=[]
    AllJoints=[]
    AllSupports=[]
    AllForces=[]
    ObjNum=0
    
    #Will need to be deleted in the future
    #form=[{u'y2': 300, u'e': 300000, u'i': 100, u'area': 10, u'servy1': 25, u'servx1': 5, u'servx2': 10, u'x2': 150, u'servy2': 25, u'y1': 300, u'x1': 75, u'type': u'member'}, {u'y2': 300, u'e': 300000, u'i': 100, u'area': 10, u'servy1': 25, u'servx1': 10, u'servx2': 20, u'x2': 300, u'servy2': 25, u'y1': 300, u'x1': 150, u'type': u'member'}, {u'y1': 300, u'servy1': 25, u'x1': 150, u'type': u'Hinge', u'servx1': 10}, {u'y1': 300, u'servy1': 25, u'x1': 75, u'type': u'YSupport', u'servx1': 5}, {u'y1': 300, u'servy1': 25, u'x1': 300, u'type': u'PinSupport', u'servx1': 20}, {u'y1': 300, u'servy1': 25, u'x1': 225, u'type': u'YSupport', u'servx1': 15}, {u'servy1': 25, u'servx1': 12, u'magnitude': u'-100', u'y1': 180, u'x1': 180, u'type': u'YForce'}]
    #form=[{u'y2': 150, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 10, u'servx2': 20, u'x2': 300, u'servy2': 15, u'y1': 150, u'x1': 150, u'type': u'member'}, {u'name': u'S1', u'servy1': 15, u'servx1': 10, u'y1': 150, u'x1': 150, u'type': u'FixedSupport'}, {u'servy1': 15, u'servx1': 12, u'magnitude': u'-100', u'y1': 180, u'x1': 180, u'type': u'YForce',  u'name': u'F2'}]
    #fixed, 3 joints
    #form=[{u'y2': 450, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 5, u'servx2': 10, u'x2': 150, u'servy2': 15, u'y1': 450, u'x1': 75, u'type': u'member'}, {u'y2': 450, u'e': 300000, u'name': u'M1', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 10, u'servx2': 20, u'x2': 300, u'servy2': 15, u'y1': 450, u'x1': 150, u'type': u'member'}, {u'y2': 450, u'e': 300000, u'name': u'M2', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 20, u'servx2': 30, u'x2': 450, u'servy2': 15, u'y1': 450, u'x1': 300, u'type': u'member'}, {u'y2': 450, u'e': 300000, u'name': u'M3', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 30, u'servx2': 40, u'x2': 600, u'servy2': 15, u'y1': 450, u'x1': 450, u'type': u'member'}, {u'name': u'S4', u'servy1': 15, u'servx1': 5, u'y1': 450, u'x1':75, u'type': u'FixedSupport'}, {u'name': u'S5', u'servy1': 15, u'servx1': 40, u'y1': 450, u'x1': 600, u'type': u'FixedSupport'}, {u'name': u'P6', u'servy1': 15, u'servx1': 10, u'y1': 450, u'x1': 150, u'type': u'Hinge'}, {u'name': u'P7', u'servy1': 15, u'servx1': 20, u'y1': 450, u'x1': 300, u'type': u'Hinge'}, {u'name': u'P8', u'servy1': 15, u'servx1': 30, u'y1': 450, u'x1': 450, u'type': u'Hinge'}, {u'name': u'F9', u'servy1': 15, u'servx1': 15, u'magnitude': u'-100', u'y1': 225, u'x1': 225, u'type': u'YForce'}]
    #fixed, distributed
    #form = [{u'y2': 375, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 20, u'i': 100, u'servx1': 5, u'servx2': 25, u'x2': 375, u'servy2': 20, u'y1': 375, u'x1': 75, u'type': u'member'}, {u'slope': u'infinity', u'f1': u'2', u'f2': u'5', u'y2':0, u'r1': u'12', u'r2': u'17', u'servy1': 20, u'servx1': 17, u'servx2': 24.2, u'direction': u'Global-Y', u'x2': 1, u'servy2': 20, u'onmember': 0, u'y1': 0, u'x1': 0, u'type': u'DForce', u'name': u'D1'}, {u'name': u'S2', u'servy1': 20, u'servx1': 5, u'y1': 375, u'x1': 75, u'type': u'FixedSupport'}]
    
    for x in form:
        print(x['type'])
        if(x['type']=='member'):
            tempmember = member(x['servx1'], x['servy1'], x['servx2'], x['servy2'], x['i'], x['e'], x['area'], x['name'])
            AllParts.append(tempmember)
            AllMembers.append(tempmember)
        elif(x['type']=='Hinge' or x['type']=='FixedJoint'):
            tempjoint = joint(x['servx1'], x['servy1'], x['type'], x['name'])
            AllParts.append(tempjoint)
            AllJoints.append(tempjoint)
        elif(x['type']=='XSupport' or x['type']=='YSupport' or x['type']=='PinSupport' or x['type']=='FixedSupport'):
            tempsupport = support(x['servx1'], x['servy1'], x['type'],x['name'])
            AllParts.append(tempsupport)
            AllSupports.append(tempsupport)
        elif(x['type']=='Xforce' or x['type']=='YForce' or x['type']=='MSupport' or x['type']=='DSupport'):
            tempforce = force(x['servx1'], x['servy1'], x['type'], x['magnitude'],x['name'])
            AllParts.append(tempforce)
            AllForces.append(tempforce)
        elif(x['type']=='DForce'):
            tempdforce = dforce(x['servx1'], x['servy1'],x['servx2'], x['servy2'], x['type'], x['f1'],x['f2'],x['direction'], x['onmember'], x['r1'], x['r2'], x['slope'], x['name'])
            AllParts.append(tempdforce)
            AllForces.append(tempdforce)
        ObjNum+=1
    
    sorted(AllParts, key=attrgetter('x1','y1'))
    sorted(AllMembers, key=attrgetter('x1','y1'))
    sorted(AllJoints, key=attrgetter('x1','y1'))
    sorted(AllSupports, key=attrgetter('x1','y1'))
    sorted(AllForces, key=attrgetter('x1','y1'))
    
    answer=FindReaction(AllParts, AllMembers, AllJoints, AllSupports, AllForces)
    
    #check=42
    #AllParts=[['ihi'],['wsaasdf'],[12]]
    #temp=form[0]['x1']
    print(answer)
    return AllParts

#output = MainParse(sys.argv[1])
    




