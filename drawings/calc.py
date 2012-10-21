import randomimport random
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

class Points:
    def __init__(self):
        self.points=[]
    def add(self, x1t, y1t, partt):
        #check if point already exists (probably need to be optimized), if exist return position
        matchcount=0
        for pos1 in range(len(self.points)):
            #print('break2')
            #print(partt.type)
            #print(self.points[pos1][2].type)
            if(self.points[pos1][0]==x1t and self.points[pos1][1]==y1t and self.points[pos1][2].type=='Member' and partt.type=='Member'):
                matchcount+=1
                return pos1
            elif(self.points[pos1][0]==x1t and self.points[pos1][1]==y1t and self.points[pos1][2]==partt):
                matchcount+=1
                return pos1
        
        #add to points
        if(matchcount==0):
            temp=[x1t, y1t, partt]
            self.points.append(temp) 
            return len(self.points)-1
    def getX(self,x):
        return self.points[x][0]
    def getY(self,x):
        return self.points[x][1]
    def getPart(self,x):
        return self.points[x][2]
        
class Connections:
    #add connections (pos of the point in the points array)
    def __init__(self):
        self.connections=[]
    def add(self, c1t, c2t, membert, anglet, lengtht, forcelistt,points):
    #check if connection already exists (probably need to be optimized)
        matchcount=0
        for connection in self.connections:
            if((connection['c1']==c1t and connection['c2']==c2t) or (connection['c1']==c2t and connection['c2']==c1t)):
                matchcount+=1
        if(matchcount==0):
            if(points.getX(c1t)<=points.getX(c2t)):
                temp={'c1':c1t, 'c2':c2t, 'member':membert, 'angle':anglet, 'length':lengtht, 'forcelist':forcelistt}
                self.connections.append(temp)
            else:
                temp={'c1':c2t, 'c2':c1t, 'member':membert, 'angle':anglet, 'length':lengtht, 'forcelist':forcelistt}
                self.connections.append(temp)

class Member:
    
    def __init__(self, x1t, y1t, x2t, y2t, it, et, areat,namet):
        if( (float(min(x1t,x2t))==x1t) or (x1t==x2t and y1t==float(max(y1t,y2t)))):
            self.x1=x1t
            self.y1=y1t
            self.x2=x2t
            self.y2=y2t
            
        else:
            self.x1=x2t
            self.y1=y2t
            self.x2=x1t
            self.y2=y1t

        self.i=float(it)
        self.e=float(et)
        self.area=float(areat)
        self.length = float(sqrt(abs(self.x1-self.x2)**2+abs(self.y1-self.y2)**2))
        self.name=namet
        self.category="Member"
        
        #actual answers
        self.dx1=0
        self.dy1=0
        self.dm1=0
        self.dx2=0
        self.dy2=0
        self.dm2=0


        self.type='Member'
        self.connectpart=[]
        self.ShearDiagram=[]
    
    def Get_Details(self):
        temp={}
        temp.update({'servx1':self.x1})
        temp.update({'servy1':self.y1})
        temp.update({'servx2':self.x2})
        temp.update({'servy2':self.y2})
        
        temp.update({'dx1':self.dx1})
        temp.update({'dy1':self.dy1})
        temp.update({'dm1':self.dm1})
        temp.update({'dx2':self.dx2})
        temp.update({'dy2':self.dy2})
        temp.update({'dm2':self.dm2})
        
        temp.update({'i':self.i})
        temp.update({'e':self.e})
        temp.update({'area':self.area})
        temp.update({'length':self.length})
        temp.update({'name':self.name})
        temp.update({'type':self.type})
        temp.update({'ShearDiagram': self.ShearDiagram})
        
        temp.update({'connectpart':self.connectpart})
        

        return temp
        
        
    '''
    def addjoint (self, jointt, x1t, y1t):
        if(self.x1==x1t and self.y1==y1t):
            self.joint1={'type': jointt}
        elif(self.x2==x1t and self.y2==y1t):
            self.joint2={'type': jointt}
        #ignoring mid member joints for now
    '''   
    

class joint:
    
    def __init__(self, x1t, y1t, typet,namet):
        self.x1=float(x1t)
        self.y1=float(y1t)
        self.type=typet
        self.name=namet
        self.onmember=[]
        self.category="Joint"
        
        #actual answers
        self.dx1=0
        self.dy1=0
        self.dm1=0
    
    def Get_Details(self):
        temp={}
        temp.update({'servx1':self.x1})
        temp.update({'servy1':self.y1})
        
        temp.update({'dx1':self.dx1})
        temp.update({'dy1':self.dy1})
        temp.update({'dm1':self.dm1})

        temp.update({'name':self.name})
        temp.update({'type':self.type})
        temp.update({'onmember': self.onmember})

        return temp
        
class support:
    magx=None
    magy=None
    magm=None
    
    
    def __init__(self, x1t, y1t, typet,namet):
        self.x1=float(x1t)
        self.y1=float(y1t)
        self.type=typet
        self.name=namet
        self.onmember=[]
        
        #actual answers
        self.dx1=0
        self.dy1=0
        self.dm1=0
        self.fx1=0
        self.fy1=0
        self.fm1=0
        self.category="Support"
        
    def Get_Details(self):
        temp={}
        temp.update({'servx1':self.x1})
        temp.update({'servy1':self.y1})
        
        temp.update({'dx1':self.dx1})
        temp.update({'dy1':self.dy1})
        temp.update({'dm1':self.dm1})
        temp.update({'fx1':self.fx1})
        temp.update({'fy1':self.fy1})
        temp.update({'fm1':self.fm1})

        temp.update({'name':self.name})
        temp.update({'type':self.type})
        temp.update({'onmember': self.onmember})

        return temp
        
        
class force:
    def __init__(self, x1t, y1t, typet, magnitudet,namet):
        self.onmember=[]
        self.x1=float(x1t)
        self.y1=float(y1t)
        self.type=typet
        self.magnitude = float(magnitudet)
        self.name=namet
        self.category='Force'
        self.onmember=[]
    def getx1(self):
        return self.x1
    def gettype(self):
        return self.type
    def gety1(self):
        return self.y1
    def getmagnitude(self):
        return self.magnitude
    
    def Get_Details(self):
        temp={}
        temp.update({'servx1':self.x1})
        temp.update({'servy1':self.y1})

        temp.update({'name':self.name})
        temp.update({'category':self.category})
        temp.update({'type':self.type})
        temp.update({'magnitude':self.magnitude})
        temp.update({'onmember': self.onmember})

        return temp

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
        self.category="DForce"
    def gettype(self):
        return self.type
    
    def Get_Details(self):
        temp={}
        temp.update({'servx1':self.x1})
        temp.update({'servy1':self.y1})
        temp.update({'servx2':self.x2})
        temp.update({'servy2':self.y2})
        
        temp.update({'f1':self.f1})
        temp.update({'f2':self.f2})
        temp.update({'r1':self.r2})
        temp.update({'r2':self.r2})


        temp.update({'name':self.name})
        temp.update({'direction':self.direction})
        temp.update({'slope':self.slope})
        temp.update({'category':self.category})
        temp.update({'type':self.type})
        temp.update({'magnitude':self.magnitude})
        temp.update({'onmember': self.onmember})

        return temp

def onmember(AllParts, Part, partcount):
    allcount=0
    for Member in AllParts:
        if(Member.type=='Member'):
            #algo for testing if on member
            if(Part.x1>=Member.x1 and Part.x1<=Member.x2):
                v1=[Member.x2-Member.x1, Member.y2-Member.y1]
                v2=[Member.x2-Part.x1, Member.y2-Part.y1]
                xp = v1[0]*v2[1]-v1[1]*v2[0]
                if(xp==0):
                    #on member numbered allcount by AllParts
                    Part.onmember.append(allcount)
                    #On part numbered partcount by AllParts
                    Member.connectpart.append(partcount)
        allcount+=1

def PointsFromMember(Member, AllParts):
    templist=[]
    temp1=[Member.x1, Member.y1, Member]
    temp2=[Member.x2, Member.y2, Member]
    
    
    print(Member.x1, Member.y1, ' ', Member.x2, Member.y2)
    
    #very inefficient :/
    #check for conflicts(position and type){BUG}
    for connectpart in Member.connectpart:
        conflict=bool(False)
        
        
        #for temps in templist:
        #if it is a support type, check if it is at end of member, if not just add
        
        if (AllParts[connectpart].type=="YSupport" or AllParts[connectpart].type=="PinSupport"or AllParts[connectpart].type=="XSupport"or AllParts[connectpart].type=="FixedSupport"):
            if(AllParts[connectpart].x1==Member.x1 and AllParts[connectpart].y1==Member.y1):
                temp1[2]=AllParts[connectpart]
                conflict=bool(True)
            elif(AllParts[connectpart].x1==Member.x2 and AllParts[connectpart].y1==Member.y2):
                temp2[2]=AllParts[connectpart]
                conflict=bool(True)
        #if it is a joint type, make sure it is at end of member
        elif(AllParts[connectpart].type=='Hinge' or AllParts[connectpart].type=='FixedJoint'):
            if(AllParts[connectpart].x1==Member.x1 and AllParts[connectpart].y1==Member.y1):
                temp1[2]=AllParts[connectpart]
                conflict=bool(True)
            elif(AllParts[connectpart].x1==Member.x2 and AllParts[connectpart].y1==Member.y2):
                temp2[2]=AllParts[connectpart]
                conflict=bool(True)
            #else:
                #confilct=bool(True)
                
        #if no conflict add to templist
        if(conflict==False):
            temp=[AllParts[connectpart].x1, AllParts[connectpart].y1, AllParts[connectpart]]
            templist.append(temp)
    
    
    #templist.append(temp2)#add endpoint 2
    #sort (insertion sort?) SORT IS NOT COMPLETELY ACCURATE!! (currently sort by x ASC then y DESC, but need to sort relative to the member){BUG}
    sortlist=[]
    sortlist.append(temp1)
    pos1=0
    for pos1 in range(len(templist)):
        #if pos is greater than the last element, then just append
        if(sortlist[len(sortlist)-1][0]<templist[pos1][0] or (sortlist[len(sortlist)-1][0]==templist[pos1][0] and sortlist[len(sortlist)-1][1]>templist[pos1][1])):
            sortlist.append(templist[pos1])
        #else loop until appropriate spot
        for pos2 in range(len(sortlist)):
            if(sortlist[pos2][0]>templist[pos1][0] or (sortlist[pos2][0]==templist[pos1][0] and sortlist[pos2][1]<templist[pos1][1])):
                sortlist.insert(pos2, templist[pos1])
    #add endpoint 1 to front of list
    #sortlist.insert[0,temp1] 
    sortlist.append(temp2)
    return sortlist


def MatrixCreation(connections, points):
    pos=0
    pointrecord={}
    variable=[]
    #create a record of points and its corresponding three spots in the matrix
    for connection in connections.connections:
        if (connection['c1'] not in pointrecord):
            pointrecord.update({connection['c1']:[pos,pos+1,pos+2]})
            pos+=3
        if(connection['c2'] not in pointrecord):
            pointrecord.update({connection['c2']:[pos,pos+1,pos+2]})
            pos+=3
    
    print(pointrecord)
    
    #Generate matrix of 0s
    Matrix_K=[]
    x=0
    while x in range(pos):
        y=0
        MatrixCol_Temp=[]
        while y in range(pos):
            MatrixCol_Temp.append(0)
            y+=1
        Matrix_K.append(MatrixCol_Temp)
        x+=1
    #end Generate...
    
    
    #Generate global k matrix
    for connection in connections.connections:
        targetpoints = pointrecord[connection['c1']] + pointrecord[connection['c2']]
        #print(targetpoints)
        e=connection['member'].e
        i=connection['member'].i
        a=connection['member'].area
        l=connection['length']
        c=math.cos(connection['angle'])
        s=math.sin(connection['angle'])        

        # 00,33
        Matrix_K[targetpoints[0]][targetpoints[0]]+= (e*a/l)*c**2+((12*e*i)/(l**3))*s**2
        Matrix_K[targetpoints[3]][targetpoints[3]]+= (e*a/l)*c**2+((12*e*i)/(l**3))*s**2
        #01, 10, 34, 43
        Matrix_K[targetpoints[0]][targetpoints[1]]+= (e*a/l)*c*s-(((12*e*i)/(l**3))*s*c)
        Matrix_K[targetpoints[1]][targetpoints[0]]+= (e*a/l)*c*s-(((12*e*i)/(l**3))*s*c)
        Matrix_K[targetpoints[3]][targetpoints[4]]+= (e*a/l)*c*s-(((12*e*i)/(l**3))*s*c)
        Matrix_K[targetpoints[4]][targetpoints[3]]+= (e*a/l)*c*s-(((12*e*i)/(l**3))*s*c)
        #03,30
        Matrix_K[targetpoints[0]][targetpoints[3]]+= -((e*a/l)*c**2)-(((12*e*i)/(l**3))*s**2)
        Matrix_K[targetpoints[3]][targetpoints[0]]+= -((e*a/l)*c**2)-(((12*e*i)/(l**3))*s**2)
        #04,40,31,13
        Matrix_K[targetpoints[0]][targetpoints[4]]+= -((e*a/l)*c*s)+(((12*e*i)/(l**3))*s*c)
        Matrix_K[targetpoints[4]][targetpoints[0]]+= -((e*a/l)*c*s)+(((12*e*i)/(l**3))*s*c)
        Matrix_K[targetpoints[3]][targetpoints[1]]+= -((e*a/l)*c*s)+(((12*e*i)/(l**3))*s*c)
        Matrix_K[targetpoints[1]][targetpoints[3]]+= -((e*a/l)*c*s)+(((12*e*i)/(l**3))*s*c)
        #11,44
        Matrix_K[targetpoints[1]][targetpoints[1]]+= (e*a/l)*s*s+((12*e*i)/(l**3))*c*c
        Matrix_K[targetpoints[4]][targetpoints[4]]+= (e*a/l)*s*s+((12*e*i)/(l**3))*c*c
        #14,41
        Matrix_K[targetpoints[1]][targetpoints[4]]+= -(e*a/l)*s*s-(((12*e*i)/(l**3))*c*c)
        Matrix_K[targetpoints[4]][targetpoints[1]]+= -(e*a/l)*s*s-(((12*e*i)/(l**3))*c*c)
        #02,20,05,50
        Matrix_K[targetpoints[0]][targetpoints[2]]+= -(6*e*i/l**2)*s
        Matrix_K[targetpoints[2]][targetpoints[0]]+= -(6*e*i/l**2)*s
        Matrix_K[targetpoints[0]][targetpoints[5]]+= -(6*e*i/l**2)*s
        Matrix_K[targetpoints[5]][targetpoints[0]]+= -(6*e*i/l**2)*s
        #12,21,15,51
        Matrix_K[targetpoints[1]][targetpoints[2]]+= (6*e*i/l**2)*c
        Matrix_K[targetpoints[2]][targetpoints[1]]+= (6*e*i/l**2)*c
        Matrix_K[targetpoints[1]][targetpoints[5]]+= (6*e*i/l**2)*c
        Matrix_K[targetpoints[5]][targetpoints[1]]+= (6*e*i/l**2)*c
        #32,35,53, 23
        Matrix_K[targetpoints[3]][targetpoints[2]]+= (6*e*i/l**2)*s
        Matrix_K[targetpoints[3]][targetpoints[5]]+= (6*e*i/l**2)*s
        Matrix_K[targetpoints[5]][targetpoints[3]]+= (6*e*i/l**2)*s
        #42,45,54 , 24
        Matrix_K[targetpoints[4]][targetpoints[2]]+= -(6*e*i/l**2)*c
        Matrix_K[targetpoints[4]][targetpoints[5]]+= -(6*e*i/l**2)*c
        Matrix_K[targetpoints[5]][targetpoints[4]]+= -(6*e*i/l**2)*c
        #22,55
        Matrix_K[targetpoints[2]][targetpoints[2]]+= (4*e*i/l)
        Matrix_K[targetpoints[5]][targetpoints[5]]+= (4*e*i/l)
        #25,52
        Matrix_K[targetpoints[2]][targetpoints[5]]+= (2*e*i/l)
        Matrix_K[targetpoints[5]][targetpoints[2]]+= (2*e*i/l)
    
    
    
    ForceVector=[]
    CheckedPoints=[]
    Force_Point_Assoc=[]
    x=0
    #create empty forcevector
    while x in range(pos):
        ForceVector.append(0)
        x+=1
    #for f variable identification purposes(Not sure if needed completely, but just in case)
    f=0
    #generate force matrix
    for connection in connections.connections:
        #check so wont have to repeat
        if(connection['c1'] not in CheckedPoints):
            #For Fixed Support
            print('one', f, points.getPart(connection['c1']).type)
            if(points.getPart(connection['c1']).type=='FixedSupport'):
                #x direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c1']][0]]=x
                temp=[x,points.getPart(connection['c1']),'x']
                Force_Point_Assoc.append(temp)                
                f+=1
                #y direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c1']][1]]=x
                temp=[x,points.getPart(connection['c1']),'y']
                Force_Point_Assoc.append(temp) 
                f+=1
                #m direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c1']][2]]=x
                temp=[x,points.getPart(connection['c1']),'m']
                Force_Point_Assoc.append(temp) 
                f+=1
            #For X Support
            if(points.getPart(connection['c1']).type=='XSupport'):
                #x direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c1']][0]]=x
                temp=[x,points.getPart(connection['c1']),'x']
                Force_Point_Assoc.append(temp) 
                f+=1
            #For Y Support
            if(points.getPart(connection['c1']).type=='YSupport'):
                #y direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c1']][1]]=x
                temp=[x,points.getPart(connection['c1']),'y']
                Force_Point_Assoc.append(temp) 
                f+=1
            #For Pin Support
            if(points.getPart(connection['c1']).type=='PinSupport'):
                #x direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c1']][0]]=x
                temp=[x,points.getPart(connection['c1']),'x']
                Force_Point_Assoc.append(temp) 
                print(f)
                print(ForceVector)
                f+=1
                #y direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c1']][1]]=x
                temp=[x,points.getPart(connection['c1']),'y']
                Force_Point_Assoc.append(temp) 
                f+=1
            #Add to list of points that have been checked
            CheckedPoints.append(connection['c1'])
            
            #check so wont have to repeat
        
        if(connection['c2'] not in CheckedPoints):
            print('two',f, points.getPart(connection['c2']).type)
            #For Fixed Support
            if(points.getPart(connection['c2']).type=='FixedSupport'):
                #x direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c2']][0]]=x
                temp=[x,points.getPart(connection['c2']),'x']
                Force_Point_Assoc.append(temp) 
                f+=1
                #y direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c2']][1]]=x
                temp=[x,points.getPart(connection['c2']),'y']
                Force_Point_Assoc.append(temp) 
                f+=1
                #m direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c2']][2]]=x
                temp=[x,points.getPart(connection['c2']),'m']
                Force_Point_Assoc.append(temp) 
                f+=1
            #For X Support
            if(points.getPart(connection['c2']).type=='XSupport'):
                #x direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c2']][0]]=x
                temp=[x,points.getPart(connection['c2']),'x']
                Force_Point_Assoc.append(temp) 
                f+=1
            #For Y Support
            if(points.getPart(connection['c2']).type=='YSupport'):
                #y direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c2']][1]]=x
                temp=[x,points.getPart(connection['c2']),'y']
                Force_Point_Assoc.append(temp) 
                f+=1
            #For Pin Support
            if(points.getPart(connection['c2']).type=='PinSupport'):
                #x direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c2']][0]]=x
                temp=[x,points.getPart(connection['c2']),'x']
                Force_Point_Assoc.append(temp) 
                print(f)
                f+=1
                #y direction unknown
                tempname='F'+str(f)
                x=Symbol(tempname)
                variable.append(x)
                ForceVector[pointrecord[connection['c2']][1]]=x
                temp=[x,points.getPart(connection['c2']),'y']
                Force_Point_Assoc.append(temp)
                print(f) 
                f+=1
            #Add to list of points that have been checked
            CheckedPoints.append(connection['c2'])
        #NOW THAT BOTH POINTS HAVE BEEN CHECKED FOR FORCES, NOW FOR FORCELIST
        
        
        #IF FORCES__________________________
        #Loop through the list of forces
        for force in connection['forcelist']:
            #if x force
            if (force.gettype()=="XForce"):
                #if force is on c1
                if(force.getx1()==points.getX(connection['c1']) and force.gety1()==points.getY(connection['c1'])):
                    ForceVector[pointrecord[connection['c1']][0]]+=force.getmagnitude()
                #if force is on c2
                if(force.getx1()==points.getX(connection['c2']) and force.gety1()==points.getY(connection['c2'])):
                    ForceVector[pointrecord[connection['c2']][0]]+=force.getmagnitude()
           #if  y force
            if (force.gettype()=="YForce"):
                #if force is on c1
                if(force.getx1()==points.getX(connection['c1']) and force.gety1()==points.getY(connection['c1'])):
                    ForceVector[pointrecord[connection['c1']][1]]+=force.getmagnitude()
                #if force is on c2
                if(force.getx1()==points.getX(connection['c2']) and force.gety1()==points.getY(connection['c2'])):
                    ForceVector[pointrecord[connection['c2']][1]]+=force.getmagnitude()
            #if  m force
            if (force.gettype()=="MForce"):
                #if force is on c1
                if(force.getx1()==points.getX(connection['c1']) and force.gety1()==points.getY(connection['c1'])):
                    ForceVector[pointrecord[connection['c1']][2]]+=force.getmagnitude()
                #if force is on c2
                if(force.getx1()==points.getX(connection['c2']) and force.gety1()==points.getY(connection['c2'])):
                    ForceVector[pointrecord[connection['c2']][2]]+=force.getmagnitude()
    
    
    
    #generate deflection vector
    DeflectionVector=[]
    Deflection_Point_Assoc=[]
    CheckedPoints2=[]
    x=0
    #create empty forcevector
    while x in range(pos):
        DeflectionVector.append(0)
        x+=1
    #for f variable identification purposes(Not sure if needed completely, but just in case)
    d=0
    #generate deflection vector
    for connection in connections.connections:
        
        #print(points.getPart(connection['c1']).type)
        #check so wont have to repeat
        if(connection['c1'] not in CheckedPoints2):
            print('d_one', d,connection['c1'] )
            #For X Support
            if(points.getPart(connection['c1']).type=='XSupport'):
                #y direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][1]]=x
                temp=[x,points.getPart(connection['c1']),'y']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][2]]=x
                temp=[x,points.getPart(connection['c1']),'m']
                Deflection_Point_Assoc.append(temp) 
                d+=1
            #For Y Support
            if(points.getPart(connection['c1']).type=='YSupport'):
                #X direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][0]]=x
                temp=[x,points.getPart(connection['c1']),'x']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][2]]=x
                temp=[x,points.getPart(connection['c1']),'m']
                Deflection_Point_Assoc.append(temp) 
                d+=1
            #For Pin Support
            if(points.getPart(connection['c1']).type=='PinSupport'):
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][2]]=x
                temp=[x,points.getPart(connection['c1']),'m']
                Deflection_Point_Assoc.append(temp) 
                d+=1
            #For Members
            if(points.getPart(connection['c1']).type=='Member'):
                #X direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][0]]=x
                temp=[x,points.getPart(connection['c1']),'x1']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #y direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][1]]=x
                temp=[x,points.getPart(connection['c1']),'y1']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][2]]=x
                temp=[x,points.getPart(connection['c1']),'m1']
                Deflection_Point_Assoc.append(temp) 
                d+=1
            #For Hinge
            if(points.getPart(connection['c1']).type=='Hinge'):
                #X direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][0]]=x
                temp=[x,points.getPart(connection['c1']),'x']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #y direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][1]]=x
                temp=[x,points.getPart(connection['c1']),'y']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][2]]=x
                temp=[x,points.getPart(connection['c1']),'m']
                Deflection_Point_Assoc.append(temp) 
                d+=1
            #For Fixed Joint
            if(points.getPart(connection['c1']).type=='FixedJoint'):
                #X direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][0]]=x
                temp=[x,points.getPart(connection['c1']),'x']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #y direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][1]]=x
                temp=[x,points.getPart(connection['c1']),'y']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c1']][2]]=x
                temp=[x,points.getPart(connection['c1']),'m']
                Deflection_Point_Assoc.append(temp) 
                d+=1

            CheckedPoints2.append(connection['c1'])
            
        #For point 2__________________________________________________
        if(connection['c2'] not in CheckedPoints2):
            #print(d,connection['c2'] )
            print('d-two',d, points.getPart(connection['c2']).type)
            #for X support
            if(points.getPart(connection['c2']).type=='XSupport'):
                #y direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][1]]=x
                temp=[x,points.getPart(connection['c2']),'y']
                Deflection_Point_Assoc.append(temp) 
                print(d)
                d+=1
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][2]]=x
                temp=[x,points.getPart(connection['c2']),'m']
                Deflection_Point_Assoc.append(temp) 
                print(d)
                d+=1
            #For Y Support
            if(points.getPart(connection['c2']).type=='YSupport'):
                #X direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][0]]=x
                temp=[x,points.getPart(connection['c2']),'x']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][2]]=x
                temp=[x,points.getPart(connection['c2']),'m']
                Deflection_Point_Assoc.append(temp) 
                d+=1
            #For Pin Support
            if(points.getPart(connection['c2']).type=='PinSupport'):
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][2]]=x
                temp=[x,points.getPart(connection['c2']),'m']
                Deflection_Point_Assoc.append(temp) 
                d+=1
            #For Members
            if(points.getPart(connection['c2']).type=='Member'):
                #X direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][0]]=x
                temp=[x,points.getPart(connection['c2']),'x2']
                Deflection_Point_Assoc.append(temp)
                d+=1
                #y direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][1]]=x
                temp=[x,points.getPart(connection['c2']),'y2']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][2]]=x
                temp=[x,points.getPart(connection['c2']),'m2']
                Deflection_Point_Assoc.append(temp)
                d+=1
            #For Hinge
            if(points.getPart(connection['c2']).type=='Hinge'):
                #X direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][0]]=x
                temp=[x,points.getPart(connection['c2']),'x']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #y direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][1]]=x
                temp=[x,points.getPart(connection['c2']),'y']
                Deflection_Point_Assoc.append(temp)
                d+=1
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][2]]=x
                temp=[x,points.getPart(connection['c2']),'m']
                Deflection_Point_Assoc.append(temp) 
                d+=1
            #For Fixed Joint
            if(points.getPart(connection['c2']).type=='FixedJoint'):
                #X direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][0]]=x
                temp=[x,points.getPart(connection['c2']),'x']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #y direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][1]]=x
                temp=[x,points.getPart(connection['c2']),'y']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                #m direction unknown
                tempname='D'+str(d)
                x=Symbol(tempname)
                variable.append(x)
                DeflectionVector[pointrecord[connection['c2']][2]]=x
                temp=[x,points.getPart(connection['c2']),'m']
                Deflection_Point_Assoc.append(temp) 
                d+=1
                
            CheckedPoints2.append(connection['c2'])
            
                
            

    ForceVector=Matrix(ForceVector)
    DeflectionVector=Matrix(DeflectionVector)
    KMatrix= Matrix(Matrix_K)
    
    '''
    print("fpa")
    print(Force_Point_Assoc)
    print("dpa")
    print(Deflection_Point_Assoc)
    print('checkedpoints')
    print(CheckedPoints, CheckedPoints2)
    '''

    return KMatrix, pointrecord , ForceVector, DeflectionVector, variable, Force_Point_Assoc, Deflection_Point_Assoc


def DistanceFromStart(Part1, Part2):
    length = float(abs(sqrt(abs( (Part2.x1-Part1.x1)**2+(Part2.y1-Part1.y1)**2))))
    return length

def ForceGlobalToLocal(member,Force, AorS):
    if(member.x2-member.x1):
        angle=math.pi/2
    else:
        angle = math.atan(float(member.y2-member.y1)/float(member.x2-member.x1))
    #if x force
    if(Force.type=="XForce"):
        if(AorS=="Axial"):
            axial=float(Force.magnitude*(sin(angle)))
            return axial
        else:
            shear=float(Force.magnitude*(cos(angle)))
            return shear
    #if y force
    if(Force.type=="YForce"):
        if(AorS=="Axial"):
            axial=float(Force.magnitude*(cos(angle)))
            return axial
        else:
            shear=float(Force.magnitude*(sin(angle)))
            return shear
    
def ReactionGlobalToLocal(member, direction, magnitude, AorS):
    if(member.x2-member.x1==0):
        angle=math.pi/2
    else:
        angle = math.atan(float(member.y2-member.y1)/float(member.x2-member.x1))
    
    #if Y direction
    if(direction=="Y"):
        if(AorS=="Axial"):
            axial=float(magnitude*(cos(angle)))
            return axial
        else:
            shear=float(magnitude*(sin(angle)))
            return shear
    
    if(direction=="X"):
        if(AorS=="Axial"):
            axial=float(magnitude*(sin(angle)))
            return axial
        else:
            shear=float(magnitude*(cos(angle)))
            return shear

def ForceDiagram(AllParts):
    for member in AllParts:
        if (member.type=='member'):
            XForceDiagram=[]
            YForceDiagram=[]
            MForceDiagram=[]
            #get reaction forces and applied loads
            for connectpart in member.connectpart:
                #calc distance from beginning ot the part
                distance=DistanceFromStart(Member,connectpart)
                if(connectpart.category=="Force"):
                    if(connectpart.type=="XForce"):
                        temp=[]
                        temp.append(distance)
                        temp.append(connectpart.magnitude)
                        XForceDiagram.append(temp)
                    if(connectpart.type=="YForce"):
                        temp=[]
                        temp.append(distance)
                        temp.append(connectpart.magnitude)
                        YForceDiagram.append(temp)
                    if(connectpart.type=="MForce"):
                        temp=[]
                        temp.append(distance)
                        temp.append(connectpart.magnitude)
                        MForceDiagram.append(temp)
                if(connectpart.category=="DForce"):
                    temp=[]
          
    return 0

def ShearDiagram(AllParts):
    for member in AllParts:
        #go through all the members
        if (member.type=='Member'):
            ShearDiagram=[]
            temp=[0.0,0.0]
            ShearDiagram.append(temp)
            #get reaction forces and applied loads, ignore dforce for now
            pos1=0
            while pos1 in range(len(member.connectpart)):
                #if the first 
                if(pos1==0 and (AllParts[member.connectpart[pos1]].category=="Force" or AllParts[member.connectpart[pos1]].category=="Support")):
                    distance=DistanceFromStart(member,AllParts[member.connectpart[pos1]])
                    temp1=[distance,0.0]
                    ShearDiagram.append(temp1)
                    if(AllParts[member.connectpart[pos1]].category=="Force"):
                        if(AllParts[member.connectpart[pos1]].type=="XForce"):
                            tempforce=ForceGlobalToLocal(member, AllParts[member.connectpart[pos1]], "Shear")
                            temp=[distance, temforce]
                            ShearDiagram.append(temp)                            
                        if(AllParts[member.connectpart[pos1]].type=="YForce"):
                            tempforce=ForceGlobalToLocal(member, AllParts[member.connectpart[pos1]], "Shear")
                            temp=[distance, temforce]
                            ShearDiagram.append(temp)
                    if(AllParts[member.connectpart[pos1]].category=="Support"):
                        tempforce1=ReactionGlobalToLocal(member, 'X', AllParts[member.connectpart[pos1]].fx1, "Shear")
                        tempforce2=ReactionGlobalToLocal(member, 'Y', AllParts[member.connectpart[pos1]].fy1, "Shear")
                        tempforce=tempforce1+tempforce2
                        if(tempforce!=0):
                            temp=[distance, tempforce]
                            ShearDiagram.append(temp) 
                            
                #if not the first one
                elif(AllParts[member.connectpart[pos1]].category=="Force" or AllParts[member.connectpart[pos1]].category=="Support"):
                    #before the force is applied
                    prevforce=ShearDiagram[len(ShearDiagram)-1][1]
                    distance=DistanceFromStart(member,AllParts[member.connectpart[pos1]])
                    tempprev=[distance,prevforce]
                    ShearDiagram.append(tempprev)
                        
                    #after force is applied
                    if(AllParts[member.connectpart[pos1]].category=="Force"):
                        if(AllParts[member.connectpart[pos1]].type=="XForce"):
                            tempforce=ForceGlobalToLocal(member, AllParts[member.connectpart[pos1]], "Shear")
                            tempforce=prevforce+tempforce
                            temp=[distance, tempforce]
                            ShearDiagram.append(temp)                            
                        if(AllParts[member.connectpart[pos1]].type=="YForce"):
                            tempforce=ForceGlobalToLocal(member, AllParts[member.connectpart[pos1]], "Shear")
                            tempforce=prevforce+tempforce
                            temp=[distance, tempforce]
                            ShearDiagram.append(temp)
                    if(AllParts[member.connectpart[pos1]].category=="Support"):
                        tempforce1=ReactionGlobalToLocal(member, 'X', AllParts[member.connectpart[pos1]].fx1, "Shear")
                        tempforce2=ReactionGlobalToLocal(member, 'Y', AllParts[member.connectpart[pos1]].fy1, "Shear")
                        tempforce=tempforce1+tempforce2
                        tempforce=prevforce+tempforce
                        temp=[distance, tempforce]
                        ShearDiagram.append(temp)
                            
                #print(ShearDiagram)
                member.ShearDiagram=ShearDiagram
                pos1+=1
                    
    
    return 0

def AxialDiagram():
    return 0

def MomentDiagram():
    return 0

def DeflectionDiagram():
    return 0

def FindReaction(AllParts, AllMembers, AllJoints, AllSupports, AllForces):
    #KIND OF DONE, BUT A LOT OF BUGS (DITCHING THIS EFFORT FOR MSA... FOR NOW)
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
        if (support.magm ==None and support.type=='FixedSupport'):
            tempname='m'+str(mcount)
            m=Symbol(tempname)
            unknown.append(m)
            unknowny.append(m)
            
            TempZMoment+=m
            SumY+=0*m
            mcount+=1
            ycount+=1
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
            if(support.magm==None and support.type=='FixedSupport'):
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
    mcount=0
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
        if(support.magm==None and support.type=='FixedSupport'):
            support.magm=answery[unknowny[ycount]]
            answer[str(scount)+'m']=answery[unknowny[ycount]]
            ycount+=1
            
        scount+=1
            
    return (answer)



def YShearCalc(Member,AllParts):
    #NOT BY ANY MEANS CLOSE TO BEING DONE, just a PLACEHOLDER FOR NOW
    TempParts=[]
    for x in Member.connectpart:
        TempParts.append(AllParts[x])
    
    sorted(TempParts, key=attrgetter('x1','y1'))
    TempParts[0]
    
def MainParse(form):
    
    #DPs = simplejson.loads(form)
    AllParts=[]
    AllMembers=[]
    AllJoints=[]
    AllSupports=[]
    AllForces=[]
    points= Points()
    connections = Connections()
    ObjNum=0
    
    #Will need to be deleted in the future
    #form=[{u'y2': 300, u'e': 300000, u'i': 100, u'area': 10, u'servy1': 25, u'servx1': 5, u'servx2': 10, u'x2': 150, u'servy2': 25, u'y1': 300, u'x1': 75, u'type': u'member'}, {u'y2': 300, u'e': 300000, u'i': 100, u'area': 10, u'servy1': 25, u'servx1': 10, u'servx2': 20, u'x2': 300, u'servy2': 25, u'y1': 300, u'x1': 150, u'type': u'member'}, {u'y1': 300, u'servy1': 25, u'x1': 150, u'type': u'Hinge', u'servx1': 10}, {u'y1': 300, u'servy1': 25, u'x1': 75, u'type': u'YSupport', u'servx1': 5}, {u'y1': 300, u'servy1': 25, u'x1': 300, u'type': u'PinSupport', u'servx1': 20}, {u'y1': 300, u'servy1': 25, u'x1': 225, u'type': u'YSupport', u'servx1': 15}, {u'servy1': 25, u'servx1': 12, u'magnitude': u'-100', u'y1': 180, u'x1': 180, u'type': u'YForce'}]
    #form=[{u'y2': 150, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 10, u'servx2': 20, u'x2': 300, u'servy2': 15, u'y1': 150, u'x1': 150, u'type': u'member'}, {u'name': u'S1', u'servy1': 15, u'servx1': 10, u'y1': 150, u'x1': 150, u'type': u'FixedSupport'}, {u'servy1': 15, u'servx1': 12, u'magnitude': u'-100', u'y1': 180, u'x1': 180, u'type': u'YForce',  u'name': u'F2'}]
    #fixed, 3 joints
    #form=[{u'y2': 450, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 5, u'servx2': 10, u'x2': 150, u'servy2': 15, u'y1': 450, u'x1': 75, u'type': u'member'}, {u'y2': 450, u'e': 300000, u'name': u'M1', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 10, u'servx2': 20, u'x2': 300, u'servy2': 15, u'y1': 450, u'x1': 150, u'type': u'member'}, {u'y2': 450, u'e': 300000, u'name': u'M2', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 20, u'servx2': 30, u'x2': 450, u'servy2': 15, u'y1': 450, u'x1': 300, u'type': u'member'}, {u'y2': 450, u'e': 300000, u'name': u'M3', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 30, u'servx2': 40, u'x2': 600, u'servy2': 15, u'y1': 450, u'x1': 450, u'type': u'member'}, {u'name': u'S4', u'servy1': 15, u'servx1': 5, u'y1': 450, u'x1':75, u'type': u'FixedSupport'}, {u'name': u'S5', u'servy1': 15, u'servx1': 40, u'y1': 450, u'x1': 600, u'type': u'FixedSupport'}, {u'name': u'P6', u'servy1': 15, u'servx1': 10, u'y1': 450, u'x1': 150, u'type': u'Hinge'}, {u'name': u'P7', u'servy1': 15, u'servx1': 20, u'y1': 450, u'x1': 300, u'type': u'Hinge'}, {u'name': u'P8', u'servy1': 15, u'servx1': 30, u'y1': 450, u'x1': 450, u'type': u'Hinge'}, {u'name': u'F9', u'servy1': 15, u'servx1': 15, u'magnitude': u'-100', u'y1': 225, u'x1': 225, u'type': u'YForce'}]
    #fixed, distributed
    #form = [{u'y2': 375, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 20, u'i': 100, u'servx1': 5, u'servx2': 25, u'x2': 375, u'servy2': 20, u'y1': 375, u'x1': 75, u'type': u'member'}, {u'slope': u'infinity', u'f1': u'2', u'f2': u'5', u'y2':0, u'r1': u'12', u'r2': u'17', u'servy1': 20, u'servx1': 17, u'servx2': 24.2, u'direction': u'Global-Y', u'x2': 1, u'servy2': 20, u'onmember': 0, u'y1': 0, u'x1': 0, u'type': u'DForce', u'name': u'D1'}, {u'name': u'S2', u'servy1': 20, u'servx1': 5, u'y1': 375, u'x1': 75, u'type': u'FixedSupport'}]
    
    #fixed, joint, distributed, y  (NO SLOPE!!!?!?)
    #form=[{u'y2': 300, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 25, u'i': 100, u'servx1': 5, u'servx2': 15, u'x2': 225, u'servy2': 25, u'y1': 300, u'x1': 75, u'type': u'member'}, {u'y2': 300, u'e': 300000, u'name': u'M1', u'area': 10, u'servy1': 25, u'i': 100, u'servx1': 15, u'servx2': 25, u'x2': 375, u'servy2': 25, u'y1': 300, u'x1': 225, u'type': u'member'}, {u'name': u'S2', u'servy1': 25, u'servx1': 25, u'y1': 300, u'x1': 375, u'type': u'YSupport'}, {u'name': u'S3', u'servy1': 25, u'servx1': 5, u'y1': 300, u'x1': 75, u'type': u'FixedSupport'}, {u'slope': u'infinity', u'f1': u'1', u'f2': u'1', u'y2': 0, u'r1': u'5', u'r2': u'8', u'servy1': 25, u'servx1': 20, u'servx2': 24.666666666666668, u'direction': u'Global-Y', u'x2': 1, u'servy2': 25, u'onmember': 1, u'y1': 0, u'x1': 0, u'type': u'DForce', u'name': u'D4'}, {u'f1': 1, u'f2': 1, u'y2': 0, u'r1': 0, u'r2': 1,u'servy1': 0, u'servx1': 0, u'servx2': 1, u'direction': u'Global-Y', u'x2': 1, u'servy2': 0, u'onmember': 0, u'y1': 0, u'x1': 0, u'type': u'DForce', u'name': u'D5'}, {u'name': u'P6', u'servy1': 25, u'servx1': 15, u'y1': 300, u'x1': 225, u'type': u'Hinge'}]
    #same as above kind of(not working, not able to solve for some reason)
    #form=[{u'y2': 225, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 10, u'i': 100, u'servx1': 10, u'servx2': 40, u'x2': 600, u'servy2': 10, u'y1': 225, u'x1': 150, u'type': u'member'}, {u'y2': 225, u'e': 300000, u'name': u'M1', u'area': 10, u'servy1': 10, u'i': 100, u'servx1': 40, u'servx2': 50, u'x2': 750, u'servy2':10, u'y1': 225, u'x1': 600, u'type': u'member'}, {u'name': u'S2', u'servy1': 10, u'servx1': 10, u'y1': 225, u'x1': 150, u'type': u'FixedSupport'}, {u'name': u'P3', u'servy1': 10, u'servx1': 40, u'y1': 225, u'x1': 600, u'type': u'Hinge'}, {u'name': u'S4', u'servy1': 10, u'servx1': 50, u'y1': 225, u'x1': 750, u'type': u'YSupport'}, {u'slope': u'infinity', u'f1': u'1', u'f2': u'5', u'y2': 0, u'r1': u'3', u'r2': u'6', u'servy1': 10, u'servx1': 13, u'servx2': 16, u'direction': u'Global-Y', u'x2': 1, u'servy2': 10, u'onmember': 0, u'y1': 0, u'x1': 0, u'type':u'DForce', u'name': u'D5'}]
    #same as above but tilted with y force (not able to solve for some reason)
    #form=[{u'y2': 150, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 5, u'i': 100, u'servx1': 15, u'servx2': 25, u'x2': 375, u'servy2': 15, u'y1': 300, u'x1': 225, u'type': u'member'}, {u'y2': 150, u'e': 300000, u'name': u'M1', u'area': 10,u'servy1': 15, u'i': 100, u'servx1': 25, u'servx2': 40, u'x2': 600, u'servy2': 15, u'y1': 150, u'x1': 375, u'type': u'member'}, {u'name': u'P2', u'servy1': 15,u'servx1': 25, u'y1': 150, u'x1': 375, u'type': u'Hinge'}, {u'name': u'S3', u'servy1': 15, u'servx1': 40, u'y1': 150, u'x1': 600, u'type': u'YSupport'}, {u'name': u'S4', u'servy1': 5, u'servx1': 15, u'y1': 300, u'x1': 225, u'type': u'FixedSupport'}, {u'name': u'F5', u'servy1': 15, u'servx1': 34, u'magnitude': u'100', u'y1': 510, u'x1': 510, u'type': u'YForce'}]
    #form=[{u'y2': 225, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 10, u'i': 100, u'servx1': 5, u'servx2': 40, u'x2': 600, u'servy2': 10, u'y1': 225, u'x1': 75, u'type': u'member'}, {u'y2': 225, u'e': 300000, u'name': u'M1', u'area': 10, u'servy1': 10, u'i': 100, u'servx1': 40, u'servx2': 60, u'x2': 900, u'servy2': 10, u'y1': 225, u'x1': 600, u'type': u'member'}, {u'name': u'P2', u'servy1': 10, u'servx1': 40, u'y1': 225, u'x1': 600, u'type': u'Hinge'}, {u'name': u'S3', u'servy1': 10, u'servx1': 5, u'y1': 225, u'x1': 75, u'type': u'PinSupport'}, {u'name': u'S4', u'servy1': 10, u'servx1': 60, u'y1': 225, u'x1': 900, u'type': u'YSupport'}, {u'name': u'F5', u'servy1': 10, u'servx1': 10, u'magnitude': u'8', u'y1':150, u'x1': 150, u'type': u'YForce'}, {u'name': u'S6', u'servy1': 10, u'servx1': 50, u'y1': 225, u'x1': 750, u'type': u'YSupport'}]
    
    #canteliver beam
    #form=[{u'y2': 375, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 20, u'i': 100, u'servx1': 20, u'servx2': 35, u'x2': 525, u'servy2': 20, u'y1': 375, u'x1': 300, u'type': u'member'}, {u'name': u'S1', u'servy1': 20, u'servx1': 20, u'y1': 375, u'x1': 300, u'type': u'FixedSupport'}, {u'name': u'F2', u'servy1': 20, u'servx1': 35, u'magnitude': u'50', u'y1': 525, u'x1': 525, u'type': u'YForce'}]
    #form=[{u'y2': 300, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 25, u'i': 100, u'servx1': 10, u'servx2': 35, u'x2': 525, u'servy2': 25, u'y1': 300, u'x1': 150, u'type': u'member'}, {u'y2': 225, u'e': 300000, u'name': u'M1', u'area': 10, u'servy1': 25, u'i': 100, u'servx1': 35, u'servx2': 45, u'x2': 675, u'servy2':30, u'y1': 300, u'x1': 525, u'type': u'member'}, {u'name': u'S2', u'servy1': 25, u'servx1': 15, u'y1': 300, u'x1': 225, u'type': u'YSupport'}, {u'name': u'S3',u'servy1': 25, u'servx1': 35, u'y1': 300, u'x1': 525, u'type': u'YSupport'}, {u'name': u'S4', u'servy1': 30, u'servx1': 45, u'y1': 225, u'x1': 675, u'type': u'XSupport'}, {u'name': u'F5', u'servy1': 25, u'servx1': 25, u'magnitude': u'100',u'y1': 375, u'x1': 375, u'type': u'YForce'}, {u'name': u'F6', u'servy1': 30, u'servx1': 45, u'magnitude': u'500', u'y1': 675, u'x1': 675, u'type': u'MForce'}]
    #Use the one below currently, 21x21
    form=[{u'y2': 150, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 25, u'i': 100, u'servx1': 15, u'servx2': 35, u'x2': 525, u'servy2': 35, u'y1': 300, u'x1': 225, u'type': u'member'}, {u'y2': 150, u'e': 300000, u'name': u'M1', u'area': 10, u'servy1': 35, u'i': 100, u'servx1': 35, u'servx2': 50, u'x2': 750, u'servy2':35, u'y1': 150, u'x1': 525, u'type': u'member'}, {u'y2': 300, u'e': 300000, u'name': u'M2', u'area': 10, u'servy1': 35, u'i': 100, u'servx1': 50, u'servx2': 35, u'x2': 525, u'servy2': 25, u'y1': 150, u'x1': 750, u'type': u'member'}, {u'y2': 375, u'e': 300000, u'name': u'M3', u'area': 10, u'servy1': 25, u'i': 100, u'servx1': 35, u'servx2': 15, u'x2': 225, u'servy2': 20, u'y1': 300, u'x1': 525, u'type': u'member'}, {u'y2': 300, u'e': 300000, u'name': u'M4', u'area': 10, u'servy1': 20, u'i': 100, u'servx1': 15, u'servx2': 15, u'x2': 225, u'servy2': 25, u'y1': 375, u'x1': 225, u'type': u'member'}, {u'name': u'P5', u'servy1': 35, u'servx1': 35, u'y1': 150, u'x1': 525, u'type': u'Hinge'}, {u'name': u'P6', u'servy1':35, u'servx1': 50, u'y1': 150, u'x1': 750, u'type': u'FixedJoint'}, {u'name': u'S7', u'servy1': 25, u'servx1': 35, u'y1': 300, u'x1': 525, u'type': u'PinSupport'}, {u'name': u'S8', u'servy1': 20, u'servx1': 15, u'y1': 375, u'x1': 225, u'type': u'FixedSupport'}, {u'name': u'F9', u'servy1': 30, u'servx1': 25, u'magnitude': u'900', u'y1': 375, u'x1': 375, u'type': u'YForce'}, {u'name': u'F10', u'servy1': 25, u'servx1': 15, u'magnitude': u'700', u'y1': 225, u'x1': 225, u'type': u'XForce'}, {u'name': u'S11', u'servy1': 35, u'servx1': 40, u'y1': 150, u'x1': 600, u'type': u'FixedSupport'}, {u'name': u'S12', u'servy1': 35, u'servx1': 45, u'y1': 150, u'x1': 675, u'type': u'PinSupport'}]
    #crazy mess
    #form=[{u'y2': 375, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 20, u'i': 100, u'servx1': 10, u'servx2': 25, u'x2': 375, u'servy2': 20, u'y1': 375, u'x1': 150, u'type': u'member'}, {u'y2': 375, u'e': 300000, u'name': u'M1', u'area': 10, u'servy1': 20, u'i': 100, u'servx1': 25, u'servx2': 35, u'x2': 525, u'servy2':20, u'y1': 375, u'x1': 375, u'type': u'member'}, {u'y2': 300, u'e': 300000, u'name': u'M2', u'area': 10, u'servy1': 20, u'i': 100, u'servx1': 35, u'servx2': 45, u'x2': 675, u'servy2': 25, u'y1': 375, u'x1': 525, u'type': u'member'}, {u'y2': 525, u'e': 300000, u'name': u'M3', u'area': 10, u'servy1': 25, u'i': 100, u'servx1': 45, u'servx2': 45, u'x2': 675, u'servy2': 10, u'y1': 300, u'x1': 675, u'type': u'member'}, {u'y2': 450, u'e': 300000, u'name': u'M4', u'area': 10, u'servy1': 10, u'i': 100, u'servx1': 45, u'servx2': 35, u'x2': 525, u'servy2': 15, u'y1': 525, u'x1': 675, u'type': u'member'}, {u'y2': 525, u'e': 300000, u'name': u'M5', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 35, u'servx2': 20, u'x2':300, u'servy2': 10, u'y1': 450, u'x1': 525, u'type': u'member'}, {u'y2': 375, u'e': 300000, u'name': u'M6', u'area': 10, u'servy1': 10, u'i': 100, u'servx1': 20, u'servx2': 10, u'x2': 150, u'servy2': 20, u'y1': 525, u'x1': 300, u'type': u'member'}, {u'name': u'P7', u'servy1': 20, u'servx1': 10, u'y1': 375, u'x1': 150,u'type': u'Hinge'}, {u'name': u'P8', u'servy1': 20, u'servx1': 35, u'y1': 375, u'x1': 525, u'type': u'Hinge'}, {u'name': u'P9', u'servy1': 15, u'servx1': 35, u'y1': 450, u'x1': 525, u'type': u'Hinge'}, {u'name': u'P10', u'servy1': 20, u'servx1': 25, u'y1': 375, u'x1': 375, u'type': u'FixedJoint'}, {u'name': u'P11', u'servy1': 25, u'servx1': 45, u'y1': 300, u'x1': 675, u'type': u'FixedJoint'}, {u'name': u'P12', u'servy1': 10, u'servx1': 45, u'y1': 525, u'x1': 675, u'type': u'FixedJoint'}, {u'name': u'P13', u'servy1': 10, u'servx1': 20, u'y1': 525, u'x1':300, u'type': u'FixedJoint'}, {u'name': u'S14', u'servy1': 20, u'servx1': 15, u'y1': 375, u'x1': 225, u'type': u'XSupport'}, {u'name': u'S15', u'servy1': 20, u'servx1': 25, u'y1': 375, u'x1': 375, u'type': u'XSupport'}, {u'name': u'S16', u'servy1': 20, u'servx1': 20, u'y1': 375, u'x1': 300, u'type': u'YSupport'}, {u'name': u'S17', u'servy1': 25, u'servx1': 45, u'y1': 300, u'x1': 675, u'type': u'YSupport'}, {u'name': u'S18', u'servy1': 10, u'servx1': 45, u'y1': 525, u'x1': 675, u'type': u'PinSupport'}, {u'name': u'S19', u'servy1': 10, u'servx1': 20, u'y1': 525, u'x1': 300, u'type': u'PinSupport'}, {u'name': u'F20', u'servy1': 12, u'servx1': 25, u'magnitude': 1, u'y1': 375, u'x1': 375, u'type': u'YForce'}, {u'name': u'F21', u'servy1': 13, u'servx1': 39, u'magnitude': 1, u'y1': 585, u'x1': 585, u'type': u'YForce'}]
    #three beam, tilted, with y and moment
    #form=[{u'y2': 300, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 20, u'i': 100, u'servx1': 10, u'servx2': 25, u'x2': 375, u'servy2': 25, u'y1': 375, u'x1': 150, u'type': u'member'}, {u'y2': 375, u'e': 300000, u'name': u'M1', u'area': 10, u'servy1': 25, u'i': 100, u'servx1': 25, u'servx2': 40, u'x2': 600, u'servy2':20, u'y1': 300, u'x1': 375, u'type': u'member'}, {u'y2': 375, u'e': 300000, u'name': u'M2', u'area': 10, u'servy1': 20, u'i': 100, u'servx1': 40, u'servx2': 50, u'x2': 750, u'servy2': 20, u'y1': 375, u'x1': 600, u'type': u'member'}, {u'name': u'S3', u'servy1': 20, u'servx1': 10, u'y1': 375, u'x1': 150, u'type': u'FixedSupport'}, {u'name': u'S4', u'servy1': 20, u'servx1': 50, u'y1': 375, u'x1': 750, u'type': u'FixedSupport'}, {u'name': u'F5', u'servy1': 25, u'servx1': 25, u'magnitude': u'100', u'y1': 375, u'x1': 375, u'type': u'YForce'}, {u'name': u'P6',u'servy1': 25, u'servx1': 25, u'y1': 300, u'x1': 375, u'type': u'FixedJoint'}, {u'name': u'P7', u'servy1': 20, u'servx1': 40, u'y1': 375, u'x1': 600, u'type': u'FixedJoint'}, {u'name': u'F8', u'servy1': 20, u'servx1': 40, u'magnitude': u'90', u'y1': 600, u'x1': 600, u'type':u'MForce'}]
    #three beam
    #form=[{u'y2': 450, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 5, u'servx2': 20, u'x2': 300, u'servy2': 15, u'y1': 450, u'x1': 75, u'type': u'member'}, {u'y2': 450, u'e': 300000, u'name': u'M1', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 20, u'servx2': 30, u'x2': 450, u'servy2': 15, u'y1': 450, u'x1': 300, u'type': u'member'}, {u'y2': 450, u'e': 300000, u'name': u'M2', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 30, u'servx2': 35, u'x2': 525, u'servy2': 15, u'y1': 450, u'x1': 450, u'type': u'member'}, {u'name': u'S3', u'servy1': 15, u'servx1': 5, u'y1': 450, u'x1': 75, u'type': u'FixedSupport'}, {u'name': u'S4', u'servy1': 15, u'servx1': 35, u'y1': 450, u'x1': 525, u'type': u'YSupport'}, {u'name': u'F5', u'servy1': 15, u'servx1': 20, u'magnitude': u'100', u'y1': 300, u'x1': 300, u'type': u'YForce'}, {u'name': u'F6', u'servy1': 15, u'servx1': 30, u'magnitude': u'50', u'y1': 450, u'x1': 450, u'type': u'MForce'}]
    #simplejson
    #form=[{u'y2': 375, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 5, u'servx2': 20, u'x2': 300, u'servy2': 20, u'y1': 450, u'x1': 75, u'type': u'member'}, {u'y2': 375, u'e': 300000, u'name': u'M1', u'area': 10, u'servy1': 20, u'i': 100, u'servx1': 20, u'servx2': 25, u'x2': 375, u'servy2': 20, u'y1': 375, u'x1': 300, u'type': u'member'}, {u'name': u'F2', u'servy1': 20, u'servx1': 25, u'magnitude': u'100', u'y1': 375, u'x1': 375, u'type': u'YForce'}, {u'name': u'S3', u'servy1': 15, u'servx1': 5, u'y1': 450, u'x1': 75, u'type': u'FixedSupport'}]
    #cantilever
    #form=[{u'y2': 150, u'e': 300000, u'name': u'M0', u'area': 10, u'servy1': 15, u'i': 100, u'servx1': 10, u'servx2': 30, u'x2': 450, u'servy2': 15, u'y1': 150, u'x1': 150, u'type': u'member'}, {u'name': u'S1', u'servy1': 15, u'servx1': 10, u'y1': 150, u'x1': 150, u'type': u'FixedSupport'}, {u'name': u'F2', u'servy1': 15, u'servx1': 30, u'magnitude': u'50', u'y1': 420, u'x1': 420, u'type': u'YForce'}]
    
    
    for x in form:
        print(x['type'])
        if(x['type']=='member'):
            tempmember = Member(x['servx1'], x['servy1'], x['servx2'], x['servy2'], x['i'], x['e'], x['area'], x['name'])
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
        elif(x['type']=='Xforce' or x['type']=='YForce' or x['type']=='MForce'):
            tempforce = force(x['servx1'], x['servy1'], x['type'], x['magnitude'],x['name'])
            AllParts.append(tempforce)
            AllForces.append(tempforce)
        elif(x['type']=='DForce'):
            tempdforce = dforce(x['servx1'], x['servy1'],x['servx2'], x['servy2'], x['type'], x['f1'],x['f2'],x['direction'], x['onmember'], x['r1'], x['r2'], x['slope'], x['name'])
            AllParts.append(tempdforce)
            AllForces.append(tempdforce)
        ObjNum+=1
    
    
    #SORT EVERYTHING BY THEIR COORDINATES.... NEED BETTER WAY TO SORT
    sorted(AllParts, key=attrgetter('x1','y1'))
    sorted(AllMembers, key=attrgetter('x1','y1'))
    sorted(AllJoints, key=attrgetter('x1','y1'))
    sorted(AllSupports, key=attrgetter('x1','y1'))
    sorted(AllForces, key=attrgetter('x1','y1'))

    
    #LOOP OVER ALL PARTS, AND ASSOCIATE EVERYTHING TO A MEMBER (NOT INCLUDING DFORCE OR MEMEBER AND ONES THAT ARE NOT ON ANY MEMBER)
    allpartcount=0
    for Part in AllParts:
        if(Part.type!='Member' and Part.type!="DForce"):
            print(Part.type)
            onmember(AllParts, Part, allpartcount)
        allpartcount+=1
    
    #JUST PRINTING/CHECKING MEMBER ASSOCIATIONS
    '''
    for Part in AllParts:
        if(Part.type=='Member'):
            print(Part.name, Part.connectpart)
        else:
            print(Part.name, Part.onmember)
    '''
    
    #start point/ connection making
    for member in AllMembers:
        sortlist=PointsFromMember(member, AllParts)
        connectionlist=[]
        for p in sortlist:
            #create point and add to connectionlist, Returns position of the point in the points array
            connectionlist.append(points.add(p[0], p[1], p[2]))
        pos1=0
        while pos1 in range(len(connectionlist)-1):
            notforce=bool(False)
            i=1
            forcelist=[]
            #check if force, if force: add to forcelist, else stop
            while notforce==False:
                if(points.getPart(connectionlist[pos1+i]).type=='XForce' or points.getPart(connectionlist[pos1+i]).type=='YForce' or points.getPart(connectionlist[pos1+i]).type=='MForce' or points.getPart(connectionlist[pos1+i]).type=='DForce'):
                    forcelist.append(points.getPart(connectionlist[pos1+i]))
                    i+=1
                else:
                    notforce=True
                
            #add connections (position of the point in the points array)
            #get length between two points
            length= abs(sqrt(abs((points.getX(connectionlist[pos1+i])-points.getX(connectionlist[pos1]))**2+(points.getY(connectionlist[pos1+i])-points.getY(connectionlist[pos1]))**2)))
            #get angle of the line, with respect to x-axis and the first point (if no slope, return 0)
            if(points.getX(connectionlist[pos1])-points.getX(connectionlist[pos1+i])==0):
                angle=math.pi/2
            else:
                angle = math.atan(float(points.getY(connectionlist[pos1])-points.getY(connectionlist[pos1+i]))/float(points.getX(connectionlist[pos1])-points.getX(connectionlist[pos1+i])))
            
            connections.add(connectionlist[pos1], connectionlist[pos1+i], member, angle, length, forcelist,points)
            pos1=pos1+i
            
    
    #answer=FindReaction(AllParts, AllMembers, AllJoints, AllSupports, AllForces)
    KMatrix, pointrecord, ForceVector, DeflectionVector, variable, Force_Point_Assoc, Deflection_Point_Assoc =MatrixCreation(connections,points)
    
    #print(KMatrix)
    #print pointrecord
    print ForceVector
    print DeflectionVector
    #print Force_Point_Assoc, Deflection_Point_Assoc
    #print variable
    
    '''
    variable=[]
    dm=[0.0,0.0,0.0,0.0,0.0,0.0]
    fm=[0.0,0.0,0.0,0.0,0.0,0.0]
    #TEMP CODE
    i=0
    while i in range(3):
        tempname='D'+str(i)
        x=Symbol(tempname)
        variable.append(x)
        dm[i]=x
        i+=1
    z=3
    while z in range(6):
        tempname='F'+str(z)
        x=Symbol(tempname)
        variable.append(x)
        fm[z]=x
        z+=1
    
    dm=Matrix(dm)
    fm=Matrix(fm)
    print(dm)
    print(fm)
    print(variable)
    k=Matrix([[200000.000000000, 0, 0, -200000.000000000, 0, 0],[0, 106666.666666667, 800000.000000000, 0, -106666.666666667, 800000.000000000],[0, 800000.000000000, 8000000.00000000, 0, 0, 4000000.00000000],[-200000.000000000, 0, 0, 200000.000000000, 0, 0],[0, -106666.666666667, -800000.000000000, 0, 106666.666666667, -800000.000000000],[0, 800000.000000000, 4000000.00000000, 0, -800000.000000000, 8000000.00000000]])
    print(k*fm)
    '''
    
    #print(KMatrix*DeflectionVector-ForceVector)
    answer=solve(KMatrix*DeflectionVector-ForceVector, variable)
    print(answer)
    
    
    print(Force_Point_Assoc)
    
    for assoc in Force_Point_Assoc:
        if(assoc[2]=='x'):
            assoc[1].fx1=float(answer[assoc[0]])
            print("here")
            #print(assoc[1].fx)
            #print(answer[assoc[0]])
        if(assoc[2]=='y'):
            assoc[1].fy1=float(answer[assoc[0]])
        if(assoc[2]=='m'):
            assoc[1].fm1=float(answer[assoc[0]])
    
    for assoc in Deflection_Point_Assoc:
        if(assoc[1].type=='Member'):
            if(assoc[2]=='x1'):
                assoc[1].dx1=float(answer[assoc[0]])
            if(assoc[2]=='x2'):
                assoc[1].dx2=float(answer[assoc[0]])
            if(assoc[2]=='y1'):
                assoc[1].dy1=float(answer[assoc[0]])
            if(assoc[2]=='y2'):
                assoc[1].dy2=float(answer[assoc[0]])
            if(assoc[2]=='m1'):
                assoc[1].dm1=float(answer[assoc[0]])
            if(assoc[2]=='m2'):
                assoc[1].dm2=float(answer[assoc[0]])
        else:
            if(assoc[2]=='x'):
                assoc[1].dx1=float(answer[assoc[0]])
            if(assoc[2]=='y'):
                assoc[1].dy1=float(answer[assoc[0]])
            if(assoc[2]=='m'):
                assoc[1].dm1=float(answer[assoc[0]])
    
    ShearDiagram(AllParts)
    
    AllJson={}
    #print member just to test
    for part in AllParts:
        temp=part.Get_Details()
        AllJson.update({part.name:temp})
    
    AllJson.update({'Calculated': 'True'})
    #print(AllJson)
    
    #Different from here down


    return AllJson