#! /usr/bin/env python3
###### THIS SCRIPT CALCULATES THE BOUNDARIES OF DURATION OF ALL GIVEN EVENTS IN THE INPUT PROGRAM. ##############
###### WRITTEN BY MARYAM RAIYAT ALIABADI ########################################################################
###### 23 JUNE 2016##############################################################################################
import sys, os
import shutil, errno
import subprocess

script_path = os.path.realpath(os.path.dirname(__file__))
InputTrace = os.path.basename(sys.argv[1])
basedir= os.getcwd()
############################################################################

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
  global InputTrace,C, classes, numofclass, basket, ETpaired, paired,FIS, group, DELTA
  
  lines = open(InputTrace).read().splitlines()
  #### removing empty members from list############################
  lines= [x for x in lines if x]
  numoflines=len (lines)
  baskets= [i for i in split_seq(lines,":::")]
  numofbasket=len(baskets)
  basket=[]
  DELTA=[[] for i in range(numofbasket)]
  for i in range (0, numofbasket):
    basket=baskets[i]
    group= GroupEvents(basket)
    DELTA[i]= CalDuration(group)
  
  ######## FLATTENING A LIST
  DELTA=[item for sublist in DELTA for item in sublist]
  DELTA= [x for x in DELTA if x]
  print ("final delta for all baskets are: ",DELTA)
  return DELTA

  
############################################################################
def GroupEvents(basket):
    C=[]
    for i in range (0, len(basket)):
        if basket[i] != '':
            C.append(basket[i].split()[1])
            C = list(set(C))
            numofclass=len(C)
            classes=[[] for i in range(numofclass)]
            for j in range (0, numofclass) :
                for i in range (0, len(basket)) :
                    if C[j] in basket[i].split() :
                        classes[j].append(basket[i])
    return classes
############################################################################
  
def CalDuration(group):
    #group=[['START_of E1 4.56', 'END_of E1 4.78', 'START_of E1 4.85', 'END_of E1 4.98'], []]
    num_group_in_basket=len(group)
    delta=[[] for i in range(len(group))]
    for j in range (0, len(group)):
        for m in range (0, len(group[j])):
            if group[j][m].split()[0]== "START_of":
                delta[j]= [ ]
                event=group[j][m].split()[1]
                delta[j]= delta[j]+ [str(event)]
                for k in range (m+1, len (group[j])):
                    if group[j][k].split()[0]=="END_of":
                        d=str((float(group[j][k].split()[2])-float(group[j][m].split()[2])))
                        group[j][k]= "--"
                        break
                delta[j]=delta[j] + [str(d)]
                group[j][m]= " -- "
        delta[j]=' '.join(delta[j])
    print ("delta", delta)
    return delta

 ###############################################################################
def MergeDurations(DELTA):
    # DELTA=['E1 1470.0', 'E2 910.0', 'E1 420.0', 'E2 1320.0', 'E1 220.0 ', 'E1 130.0', 'E2 410.0']
    f= open('TDInv.txt', 'w').close()
    FIS=[(DELTA[0].split()[0])]
    for n in range (1, len (DELTA)):
        FIS.append(DELTA[n].split()[0])
    FIS=list(set(FIS))
    DurationInv=[[] for i in range(len (FIS))]
    for n in range (0, len (FIS)):
        MergeDur=[]
        for i in range (0 , len (DELTA)):
            if FIS[n] in DELTA[i].split():
                del DELTA[i].split()[0]
                MergeDur=MergeDur+ DELTA[i].split()[1:]
        MergeDur=[float(j) for j in MergeDur]
        MergeDur=[ str(max(MergeDur))+" , "+str(min(MergeDur))]
        DurationInv[n]=[str(FIS[n]) + " :"]+ MergeDur
        TDnumber= ["TD|E Invariant ",str (n+1),". "]
        print ("Inv.", n+1,  DurationInv[n])
        TDnumber=''.join(TDnumber)

        f = open('TDInv.txt', 'a')
#f.write( '  '.join(map(lambda x: str(x), [str(TDnumber)])) + "\n")
        f.write( '  '.join(map(lambda x: str(x), DurationInv[n])) +  " (sec)"+"\n" +"\n")
        f.close()




############################################################################
def main(InputTrace):
  DELTA=readInputTETrace()
  MergeDurations(DELTA)
  ################################################################################
if __name__ == '__main__':
        main(sys.argv[1])


