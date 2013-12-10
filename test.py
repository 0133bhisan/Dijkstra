from __future__ import print_function  #for python 2
from Vertex import Vertex
from pq import Pq
import copy
import time


def main():
    adj,h=prep()

    v0=int(input("Choose a starting point "))-1
    v1=int(input("Choose1 an ending point "))-1
    ver= int(input("Press 1 to do One directional dijkstra, 2 to do two directional"))
    counter=0
    if ver==1:
        counter=doDijkstra1(adj,h,v0,v1,0)
    elif ver==2:
        counter=doDijkstra2(adj,h,v0,v1,0)
    print(counter,' : nodes visited')

    q=int(input(" Enter 1 to do it again"))
    if q==1:
        main()
        
def prep():
    f=open("ny.gr","r")
    numVertex=0
    adj=dict()                              #Adjacencylist
    h=[]                                    #hashtable
    for line in f:
        if line.split()[0]=='p':         #initialize the adjList  
            numVertex=int(line.split()[2])
            h=createHash(numVertex)
            adj=createAdjList(numVertex,h)   #passing the size of adjList            
        if line.split()[0]=='a':           
            modifyAdjList(line.split(),adj,h)      #Adding the Vertex to adjList  
    f.close()
    return adj,h
    
    
def doDijkstra1(adj,h,v0,v1,counter):
    start=time.time()
    modifyHash(h,v0,'en',0,None)
    queue=Pq([],h)
    counter+=1
    queue.insert(h[v0][1])
    switch=1    
    while(queue.size()!=0 and switch):
        v=queue.extractMin()
        for i in adj[v]:
            if h[i.label][2]=='un':           
                counter+=1
                h[i.label][2]='en'
                h[i.label][3]=h[v.label][3]+adj[v][i]
                h[i.label][4]=v
                queue.insert(i)
            elif h[i.label][2]=='en':
                newDist=h[v.label][3]+adj[v][i]
                if newDist<h[i.label][3]:
                    h[i.label][4]=v
                    h[i.label][3]=newDist
                    queue.decreaseKey(i)
        h[v.label][2]='done'
        if v.label==v1:
            switch=0
    print("Time Elapsed :",time.time()-start)
    print("Path Distance :",h[v.label][3])
    printPath1(h,h[v1][1])
    return counter

def workOnMin(adj,h0,h1,queue,best,counter): #takes in adj,h and q. processes the extractedMin until it is done. Returns 'done' v
    v=queue.extractMin()
    if h1[v.label][2]=='done':
        if best==None:
            best=v
        elif (h0[v.label][3]+h1[v.label][3])<(h0[best.label][3]+h1[best.label][3]):
            best=v
       
    for i in adj[v]:
        if h0[i.label][2]=='un':
            counter+=1
            h0[i.label][2]='en'
            h0[i.label][3]=h0[v.label][3]+adj[v][i]
            h0[i.label][4]=v
            queue.insert(i)
        elif h0[i.label][2]=='en':
            newDist=h0[v.label][3]+adj[v][i]
            if newDist<h0[i.label][3]:
                h0[i.label][4]=v
                h0[i.label][3]=newDist
        if h1[i.label][2]=='done':
            if best==None:
                best=i
            else:
                d=h0[i.label][3]+h1[i.label][3]
                if d<h0[best.label][3]+h1[best.label][3]:
                    best=i
                
                queue.decreaseKey(i)                
    h0[v.label][2]='done'        
    return h0[v.label][1],best,counter

def copyH(h0):
    h1=copy.deepcopy(h0)
    for i in range(len(h1)):
        h1[i][1]=h0[i][1]       #so that both hashtables are pointing to the same objects to keep things simple
    return h1
def printPath1(h0,destination):
    if destination==None:
        return
    printPath1(h0,h0[destination.label][4])
    print(destination.label+1)

def printPath2(h0,h1,best,destination):
    print ('Path:')
    printPath1(h0,best)
    printPath3(h1,h1[best.label][4])
    
def printPath3(h1,destination):
    if destination==None:
        return
    print(destination.label+1)
    printPath3(h1,h1[destination.label][4])
    
def doDijkstra2(adj,h0,v0,v1,counter):
    h1=copyH(h0)
    q0=Pq([],h0)
    q1=Pq([],h1)
    start=time.time()
    modifyHash(h0,v0,'en',0,None)
    modifyHash(h1,v1,'en',0,None)
    q0.insert(h0[v0][1])
    q1.insert(h1[v1][1])
    counter+=2
    best=None
    while(1):
            
            a,best,counter=workOnMin(adj,h0,h1,q0,best,counter) #a is 'done' in h0
            if h1[a.label][2]=='done':                
                sumA=h1[a.label][3]+h0[a.label][3]
                if sumA<(h0[best.label][3]+h1[best.label][3]):
                    best=a
                break
        #if (q1.size!=0):
            b,best,counter=workOnMin(adj,h1,h0,q1,best,counter) #b is done in h1
        
            if h0[b.label][2]=='done':                
                sumB=h1[b.label][3]+h0[b.label][3]
                if sumB<(h0[best.label][3]+h1[best.label][3]):
                    best=b
                break
            
    print("Time Elapsed :",time.time()-start)
    print('Path Distance: ',h0[best.label][3]+h1[best.label][3])
    printPath2(h0,h1,best,h1[v1][1])
    return counter

            
def modifyHash(h,index,s,d,v):
    h[index][2]=s
    h[index][3]=d
    h[index][4]=v
    
def createHash(n):
    h=[]
    for i in range(n):
        v=Vertex(i)
        h.append([i,v,'un',-111,None])#index of node,Vertex obj,State,dist,via, index in 
    return h

def createAdjList(n,h):
    adj={}
    for i in range(n):
        adj[h[i][1]]={}
    return adj

def modifyAdjList(d,adj,h):
    frm=int(d[1])
    to=int(d[2])
    length=int(d[3])
    adj[h[frm-1][1]][h[to-1][1]]=length

if __name__=='__main__':
    main()
