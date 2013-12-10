from __future__ import print_function   #for python Versions <3
from Vertex import Vertex


class Pq:
        #q is a minQueue
        #h is hashtable
    def __init__(self,q,h): 
        self.q=q        
        self.h=h
        self.w= dict()
   
    def size(self):
        return len(self.q)
    
    def parent(self,v):
        i=self.w[v]
        iP=((i+1)//2)-1
        if (iP>len(self.q)-1):
            return None
        else:
            return self.q[iP]
    
    def left(self,v):
        i=self.w[v]
        iL=(2*(i+1))-1
        if (iL>len(self.q)-1):
            return None
        else:
            return self.q[iL]       
    
    def right(self,v):
        i=self.w[v]
        iR= 2*(i+1)
        if (iR>len(self.q)-1):
            return None
        else:
            return self.q[iR]
    
    def minHeapify(self, v):
        #print("minheapify",v.label)
        i=self.w[v]
        l=self.left(v)
        r=self.right(v)
        smallest=v
        if l!=None :
            if self.h[l.label][3]<self.h[smallest.label][3]:
                smallest=l
        if r!=None:
            if self.h[r.label][3]<self.h[smallest.label][3]:
                smallest=r
        if smallest!=v:
            #swapping smallest and v
            p=self.w[smallest]
            self.q[i]=smallest
            self.q[p]=v
            #swapping indexNo in w:
            self.w[v]=self.w[smallest]
            self.w[smallest]=i
            self.minHeapify(v)
    
    def extractMin(self):
        if len(self.q)<1:
             print ('heap underflow')
        m=self.q[0]
        del self.w[m] #delete entry from dictionary
        
        self.q[0]=self.q[len(self.q)-1]
        self.q.pop()

        if len(self.q)>1:
            self.w[self.q[0]]=0
            self.minHeapify(self.q[0])
        return m

    
    def decreaseKey(self,v): #we assume that user updates hash table(dist) before calling decreasekey
        i=self.w[v]
        prn=self.parent(v)
        iPrn=self.w[prn]
        
        while i>0 and self.h[self.q[iPrn].label][3]>self.h[self.q[i].label][3]:
                    
            self.q[iPrn]=v
            self.q[i]=prn
            ####now swapping pos indices in self.w
            self.w[v]=iPrn
            self.w[prn]=i

            prn=self.parent(v)            
            i=self.w[v]
            iPrn=self.w[prn]
                
    def insert(self,v):
        #assume that hashtable is updated before a vertex is inserted
        self.q.append(v)
        self.w[v]=len(self.q)-1
        self.decreaseKey(v)

        


       
