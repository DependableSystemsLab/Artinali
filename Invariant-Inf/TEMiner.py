#! /usr/bin/env python3
###### THIS SCRIPT FINDS THE PAIR OF IMMIDIATE (OR ALL) EVENTS THAT FOLLOW EACH OTHER WITH SUPPORT LEVEL ##########
#############BIGGER THAN THRESHOLD ALONG WITH THE BOUNDARIES OF THEIR RELATIVE TIME. ########################
###### WRITTEN BY MARYAM RAIYAT ALIABADI ####################################################################
###### 3rd JUNE 2016#########################################################################################

import sys, os
import shutil, errno
import subprocess

script_path = os.path.realpath(os.path.dirname(__file__))
InputTrace = os.path.basename(sys.argv[1])
basedir= os.getcwd()
############################################################################

def checkInputTETrace():
	#Check for Input Trace's presence
  
  global cOpt
  srcpath = os.path.dirname(options["source"])
  try:
    f = open(os.path.join(srcpath, 'TELOG.txt'), 'r')
  except:
    print("ERROR: No TELOG.txt file in the %s directory." % srcpath)
  os.rmdir(options["dir"])
  exit(1)
#############################################################################
def split_seq(seq, sep):
  start = 0
  while start < len(seq):
    try:
      stop = start + seq[start:].index(sep)
      yield seq[start:stop]
      start = stop + 1
    except ValueError:
      yield seq[start:]
      break

#############################################################################

def readInputTETrace():
  global InputTrace,C, classes, numofclass, basket, ETpaired, paired,FIS, TE, numofbasket
  f= open('TEInv.txt', 'w').close()
  #f= open('EInv.txt', 'w').close()
  lines = open(InputTrace).read().splitlines()
  numoflines=len (lines)
  #### removing empty members from list############################
  lines= [x for x in lines if x]
  baskets= [i for i in split_seq(lines,":::")]
  return (baskets)
  
###################################################################
def  calculateTimeInv(baskets):
  numofbasket=len(baskets)
  FIS=[]
  basket=[]
  pairedBasket = [[] for i in range(numofbasket)]
  pairedTime=[[] for i in range(numofbasket)]
  for i in range (0, numofbasket):
    basket=baskets[i]
    pair, ETpaired=EventPairing(basket)
    pairedBasket.insert(i, pair)
    pairedBasket=purify(pairedBasket)
    pairedTime.insert(i, ETpaired)
    pairedTime=purify(pairedTime)
        # return (pairedBasket, pairedTime)
  return (pairedBasket,pairedTime, numofbasket)
#####################################################################
def  calculateImmidiateTimeInv(baskets):
  numofbasket=len(baskets)
  FIS=[]
  basket=[]
  pairedBasket = [[] for i in range(numofbasket)]
  pairedTime=[[] for i in range(numofbasket)]
  for i in range (0, numofbasket):
    basket=baskets[i]
    #pair, ETpaired=EventPairing(basket)
    pair, ETpaired= immidiateEpairing(basket)
    pairedBasket.insert(i, pair)
    pairedBasket=purify(pairedBasket)
    pairedTime.insert(i, ETpaired)
    pairedTime=purify(pairedTime)
  return (pairedBasket,pairedTime, numofbasket)
#####################################################################
def MergingTime (pairedBasket,pairedTime, numofbasket):
  flatPairedTime=[item for sublist in pairedTime for item in sublist]
  totalnum=len(flatPairedTime)
  FIS=pairedBasket[0]
  FISunion=pairedBasket[0]
  for i in range (1, numofbasket):
    FIS=list(set(FIS).intersection(pairedBasket[i]))
    FISunion=list(set(FISunion).union(pairedBasket[i]))
  numofFIS= len(FIS)
  MergedTime=[]
  MergedTimeU=[]
  TEinvariant=[] #[] for i in range(numofFIS)]
  Frequency=[]
  TE=[]
######### for Support less than 100#########

  support=[]
  for i in range (0, len(pairedBasket)):
    pairedBasket[i]=sorted(set(pairedBasket[i]))
  for k in range (0 , len (FISunion)):
    flag=1
    count=0
    del MergedTimeU[:]
    for i in range (0 , len(pairedBasket)) :
      for j in range (0 , len (pairedBasket[i])):
        if FISunion[k] in pairedBasket[i][j]:
          MergedTimeU.append(pairedTime[i][j].split()[1])
          print (FISunion[k])
          count=count+flag
    support.insert(k, count)
    count=0
    support[k]=(float(support[k])/len(pairedBasket))*100
  #print (support)

  for i in range (0, len(support)):
      #print (support[i])
    if support[i]< 50.0 :
      support[i]=''
      FISunion[i]=''
  support= [x for x in support if x]
  FISunion= [x for x in FISunion if x]
  # print (support)
  FIS_support=["%s%   0f" % t for t in zip(FISunion, support)]
  FIS_support=sorted(FIS_support)

####### for all support levels######################
  FISunion=sorted(FISunion)
  for n in range (0, len(FISunion)):
    del MergedTime[:]
    for i in range (0 , len(flatPairedTime)) :
        #print (flatPairedTime[i])
      if FISunion[n] in flatPairedTime[i].split():
        MergedTime.append(flatPairedTime[i].split()[1])
        print (FISunion[n],  MergedTime, flatPairedTime[i])
    if MergedTime!=[]  :#***
      MergedTime = [float(x) for x in MergedTime]
      MergedTime.sort()
   
      TEinvariant= TEinvariant+ [str (FIS_support[n]) , ":", str(max(MergedTime)), "," ,str(min (MergedTime))]
############## FINDING the Frequency of an event############
      string=list(FIS_support[n].split()[0])
      print ("string", string)
      index=string.index(">")
      name1=string[:index-1]
      name1= ''.join(name1)
      name2=string[index+1:]
      name2= ''.join(name2)
      
      if name1==name2:
        Frequency.append(list(TEinvariant))
      #print ("freq",Frequency)
      else :
        TE.append(list(TEinvariant))
      del TEinvariant[:]
  return (TE, Frequency)

#############writing invariants to the file##############

def WriteInvariantsToFile (TE):
  f = open('TEInv.txt', 'a')
  #f.write("\n"+ "############### T|E INVARIANTS ##################"+ "\n")
  for m in range (0, len(TE)):
    TEnumber= ["T|E Invariant ",str (m+1),". "]
    TEnumber=''.join(TEnumber)
    #f.write( '  '.join(map(lambda x: str(x), [str(TEnumber)])) + "\n")
    f.write( '  '.join(map(lambda x: str(x), TE[m])) + "\n" +"\n")
  f.close()
   #############################################################################

def WriteFrequenciesToFile (Frequency):
  f = open('TEInv.txt', 'a')
  f.write("\n"+ "::::::"+ "\n")
  #f.write("\n"+ "############### FREQUENCIES ##################"+ "\n")
  for n in range (0, len(Frequency)):
    Fnumber= ["Frequency ",str (n+1),". "]
    Fnumber=''.join(Fnumber)
    # f.write( '  '.join(map(lambda x: str(x), [str(Fnumber)])) + "\n")
    f.write( '  '.join(map(lambda x: str(x), Frequency[n])) + "\n" +"\n")
  f.close()

###############################################################################
def purify(l):
  for (i, sl) in enumerate(l):
    if type(sl) == list:
      l[i] = purify(sl)
  return [i for i in l if i != [] and i != '']
        
  #############################################################################
def immidiateEpairing(basket):
  numofimpairs=len(basket)-1
  Impaired=[[] for i in range(numofimpairs)]
  ImrelativeTime=[[] for i in range(numofimpairs)]
  ImETpaired=[[] for i in range(numofimpairs)]
  basket=[x for x in basket if x]
  for i in range (0, numofimpairs-1):
    ImrelativeTime[i]=abs(float((basket[i+1].split())[1])- float((basket[i].split())[1]))
    Impaired[i]=str((basket[i].split())[0])+ '->'+ str((basket[i+1].split())[0])
  ImrelativeTime=[x for x in ImrelativeTime if x]
  Impaired=[x for x in Impaired if x]
  ImETpaired=["%s%   0f" % t for t in zip(Impaired, ImrelativeTime)]
  return Impaired, ImETpaired

################################################################################

def EventPairing(basket):
  numofline= len (basket)
  numofpaires=numofline*(numofline-1)/2
  numofpaires=numofline*(numofline-1)/2
  paired=[[] for i in range(numofpaires)]
  relativeTime=[[] for i in range(numofpaires)]
  ETpaired=[[] for i in range(numofpaires)]
  k=0
  basket= [x for x in basket if x]
  for i in range (0, numofline-1):
      for j in range (i+1 ,numofline-1):
        relativeTime[k]=float((basket[j].split())[1])- float((basket[i].split())[1])
        #relativeTime.append(CalculateRelTime((basket[j].split())[1], (basket[i].split())[1]))
        paired[k]=str((basket[i].split())[0])+ '->'+ str((basket[j].split())[0])
        k=k+1
  relativeTime = [x for x in relativeTime if x]
  print ("r",relativeTime)
  paired = [x for x in paired if x]
  ETpaired=["%s%   0f" % t for t in zip(paired, relativeTime)]
  return paired,ETpaired
############################################################################
def CalculateRelTime(end, start):
    #start= '00:14:58.705781'
    #end= '01:12:58.736490'
  s=[item for sublist in start for item in sublist]
  print (s)
  temp=[''.join(s[0:2])] + [''.join(s[3:5])] +[''.join(s[6:8])] +[''.join(s[9:15])]
  s=temp
  print (s)
  sinSec=int(s[0])*60*60 + int(s[1])*60 + int(s[2]) + int(s[3])*0.000001
  print (sinSec)
  e=[item for sublist in end for item in sublist]
  temp=[''.join(e[0:2])] + [''.join(e[3:5])] +[''.join(e[6:8])] +[''.join(e[9:15])]
  e=temp
  einSec=int(e[0])*60*60 + int(e[1])*60 + int(e[2]) + int(e[3])*0.000001
  print (einSec)
  Delta= einSec-sinSec
  delta=Delta
  hour=int(delta)/3600
  min=int(delta)/60
  sec= delta- hour*3600-min*60
  microsec=delta- hour*3600-min*60-sec
  delta= str(hour) + ":" + str(min) + ":" + str(sec)
  print (Delta)
  return Delta
###############################################################################

def FindEventFrequency(baskets):
  allFreq=[[] for i in range(len(baskets))]
  for m in range (0, len(baskets)):
    basket= baskets[m]
    equalEvents=[]
    FreqClass=[[] for i in range(len(basket))]
    k=0
    flag=0
    for i in range (0, len(basket)-1):
      print(i)
      equalEvents.append(basket[i])
      for j in range (i+1, len(basket)):
        if basket[i] !='' and basket[j]!='' :
          if basket[i].split()[0] in basket[j].split() :
              equalEvents.append(basket[j])
              basket[j]=''
              flag=1
      if flag==1:
          basket[i]=''
          flag=0
          k=k+1
    
      if len(equalEvents)>=2:
        FreqClass[k]=list(equalEvents)
      del equalEvents[:]
  
    FreqClass=[x for x in FreqClass if x]
    allFreq[m]=FreqClass
        
  allFreq=[x for x in allFreq if x]
  

  for m in range (0, len(allFreq)):
    allFreq[m]= [item for sublist in allFreq[m]  for item in sublist]
  return (allFreq)
###############################################################################
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

###############################################################################

def main(InputTrace):
  
  baskets=readInputTETrace()
  pairedBasket,pairedTime, numofbasket= calculateImmidiateTimeInv(baskets)
  TE, frequency= MergingTime (pairedBasket,pairedTime, numofbasket)
  WriteInvariantsToFile (TE)
  
  allFreq= FindEventFrequency(baskets)
  pairedBasket2,pairedTime2, numofbasket= calculateImmidiateTimeInv(allFreq)
  if len(pairedBasket2)!=0 :
  
    te, Frequency= MergingTime (pairedBasket2,pairedTime2, numofbasket)
    WriteFrequenciesToFile (Frequency)
  ################################################################################
if __name__ == '__main__':
        main(sys.argv[1])


