#! /usr/bin/env python3
###### THIS SCRIPT FINDS THE SUSPICIOUS TIME FOR ALL GIVEN EVENTS OF INPUT TRACES. ######
###### WRITTEN BY MARYAM RAIYAT ALIABADI#################################################
###### 9TH JULY 2016##############################################################

import sys, os
import shutil, errno
import subprocess
Inv=os.path.basename(sys.argv[1])
InputTrace=os.path.basename(sys.argv[2])
##############################################################################
def readInputTrace():
    global InputTrace, Inv, lines1, lines2, in1, in2, DataInv, trace, baskets
    f= open('TimeAbnormality.txt', 'w').close()
    ###### taking the data invariant file ########################################
    lines1 = open(Inv).read().splitlines()
    #### removing empty members from list############################
    lines1= [x for x in lines1 if x]
    ####removing whitespace from string objects######################
    #for i in range (0 , len (lines1)):
    #lines1[i] = ''.join(lines1[i].split())
    # lines1[i].replace(" ", "")
    


    ##### taking the runtime trace ##############################################
    lines2 = open(InputTrace).read().splitlines()
    lines2= [x for x in lines2 if x]
        # for i in range (0 , len (lines2)):
        #   lines2[i] = ''.join(lines2[i].split())
        # lines2[i].replace(" ", "")
        # print (lines1, lines2)
    return  lines1, lines2



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
def AlarmAbnormality():
    
    in1, in2 = readInputTrace()
    ############ separating invariants , Pairs and Frequencies ##############
    sets = [i for i in split_seq(in1,"::::::")]
    TimeInv=[]
    Pair_set=[]
    Freq_set=[]
    Pair_set.append(sets[0])
    Pair_set=[item for sublist in Pair_set for item in sublist]
    TimeInv.append(sets[1])
    TimeInv=[item for sublist in TimeInv for item in sublist]
    #Freq_set.append(sets[2])
    # Freq_set=[item for sublist in Freq_set for item in sublist]
    #print(Inv_set)
    ############ seperating input traces#####################################
    baskets= [i for i in split_seq(in2,":::")]
    Con_abnormality=[]
    abnormality=[]
    missing_pair=[]
    anomalous_pair=[]
    TimeInv= [x for x in TimeInv if x]
    ########### checking input trace for time invariants#####################
    for i in range (0, len (baskets)):
        basket=baskets[i]
        #pair, trace= immidiateEpairing(basket)
        pair, trace= EventPairing(basket)
        #pair,trace=pairing(basket)
        for m in range (0, len(trace)):
            flag3=0
            for n in range (0, len(TimeInv)):
                flag1=0
                flag2=0
                
                if (TimeInv[n].split()[0]== trace[m].split()[0]) :
                    flag3=0
                    print (TimeInv[n].split()[2])
                    print (trace[m].split()[1])
                    if (float (trace[m].split()[1])<=float(TimeInv[n].split()[3] )):
                       if (float(trace[m].split()[1])>=float(TimeInv[n].split()[5]) ):
                            print ("absolute normality")
                       else:
                           flag1=1
                           print (" abnormality seen in lowerbound of trace ",i, trace[m])
                    else:
                        flag2=1
                        print (" abnormality seen in upperbound of trace ",i, trace[m])
                    if (flag1==1 ) or (flag2==1):
                        abnormality.append(i)
                        abnormality.append(trace[m].split())
                        abnormality.append(TimeInv[n])
                        abnormality.append('&&')
                else:
                    flag3=1
                break
           

    ######### checking input trace for absolute event pairs####

        for k in range (0, len (Pair_set)):
        # for j in range (0, len(pair)):
            if Pair_set[k] in pair :
                print ("")
            else :
                print (Pair_set[k], " is missing!")
                missing_pair.append(i)
                missing_pair.append(Pair_set[k])
                missing_pair.append('&&')

    
    abnormality= [i for i in split_seq(abnormality,"&&")]
    missing_pair=[i for i in split_seq(missing_pair,"&&")]
    anomalous_pair=[i for i in split_seq(anomalous_pair,"&&")]
    ######### removing duplicated lists from a list#########
    for n in range (0, (len(abnormality)-1)):
        if abnormality[n]==abnormality[n+1]:
            abnormality[n]=''

    for n in range (0, (len(missing_pair)-1)):
        if missing_pair[n]==missing_pair[n+1]:
            missing_pair[n]=''

    for n in range (0, (len(anomalous_pair)-1)):
        if anomalous_pair[n]==anomalous_pair[n+1]:
            anomalous_pair[n]=''
    #### removing empty members from list############################
    abnormality= [x for x in abnormality if x]
    missing_pair= [x for x in missing_pair if x]
    anomalous_pair= [x for x in anomalous_pair if x]
    ########## adding trace information####################
    for n in range (0, len(abnormality)):
        abnormality[n][0]= [" Trace # : "+ str(abnormality[n][0])]
        abnormality[n][0]=''.join(abnormality[n][0])
        abnormality[n][1]= ["Anomalous time : "+ str(': '.join(abnormality[n][1]))]
        abnormality[n][1]=''.join(abnormality[n][1])
        abnormality[n][2]= ["Violated invariant : "+ str(abnormality[n][2])]
        abnormality[n][2]=''.join(abnormality[n][2])
    print (missing_pair)
    for m in range (0, len(missing_pair)):
        missing_pair[m][0]=[" Trace # : "+ str(missing_pair[m][0])]
        missing_pair[m][0]=''.join(missing_pair[m][0])
        missing_pair[m][1]= ["Missing pair : "+ str(missing_pair[m][1])]
        missing_pair[m][1]=''.join(missing_pair[m][1])
    print (anomalous_pair)
    for m in range (0, len(anomalous_pair)):
        anomalous_pair[m][0]=[" Trace # : "+ str(anomalous_pair[m][0])]
        anomalous_pair[m][0]=''.join(anomalous_pair[m][0])
        anomalous_pair[m][1]= ["Anomalous pair : "+ str(anomalous_pair[m][1])]
        anomalous_pair[m][1]=''.join(anomalous_pair[m][1])
    ######### write the abnormalities in a file############
    for n in range (0, len(abnormality)):
        ABnumber= ["Abnormality ",str (n+1),". "]
        ABnumber=''.join(ABnumber)
        f = open('TimeAbnormality.txt', 'a')
        f.write( '  '.join(map(lambda x: str(x), [str(ABnumber)])) + "\n")
        f.write( '\n '.join(map(lambda x: str(x), abnormality[n])) + "\n" +"\n")
        f.close()
    for m in range (0, len(missing_pair)):
        ABnumber= ["Abnormality ",str (len (abnormality)+m+1),". "]
        ABnumber=''.join(ABnumber)
        f = open('TimeAbnormality.txt', 'a')
        f.write( '  '.join(map(lambda x: str(x), [str(ABnumber)])) + "\n")
        f.write( '\n '.join(map(lambda x: str(x), missing_pair[m])) + "\n" +"\n")
        f.close()

    for m in range (0, len(anomalous_pair)):
        ABnumber= ["Abnormality ",str (len (abnormality)+ len (missing_pair)+m+1),". "]
        ABnumber=''.join(ABnumber)
        f = open('TimeAbnormality.txt', 'a')
        f.write( '  '.join(map(lambda x: str(x), [str(ABnumber)])) + "\n")
        f.write( '\n '.join(map(lambda x: str(x), anomalous_pair[m])) + "\n" +"\n")
        f.close()
  #############################################################################
def immidiateEpairing(basket):
  numofimpairs=len(basket)-1
  ImrelativeTime=range(numofimpairs)
  #print ("ImrelativeTime", ImrelativeTime)
  Impaired=range(numofimpairs)
  ImETpaired=range(numofimpairs)
  basket=[x for x in basket if x]
  for i in range (0, numofimpairs):
      # print (basket[i+1].split())
      #print(basket[i+1].split())
    ImrelativeTime[i]=float((basket[i+1].split())[1])- float((basket[i].split())[1])
    Impaired[i]=str((basket[i].split())[0])+ '->'+ str((basket[i+1].split())[0])
  ImETpaired=["%s%   0f" % t for t in zip(Impaired, ImrelativeTime)]
#print ("Immidiate event time paired are: ", ImETpaired)
  return Impaired, ImETpaired
################################################################################
def pairing(basket):
    Time=[]
    pair=[]
    freq=[]
    for i in range (0, len(basket)-1):
        for j in range (i+1, len (basket)):
            if basket[i].split()[0]==basket[j].split()[0]:
                pair.append( str((basket[i].split())[0])+ '->'+ str((basket[j].split())[0]))
                Time.append(float((basket[i+1].split())[1])- float((basket[i].split())[1]))
                break
        i=j
    freq=["%s%   0f" % t for t in zip(pair, Time)]
    print ("freq ",freq)
    return pair,freq
################################################################################

def EventPairing(basket):
  numofline= len (basket)
  #print (numofline)
  numofpaires=numofline*(numofline-1)/2
  paired=[]#range(numofpaires)
  relativeTime=[]#range(numofpaires)
  ETpaired=[]#range(numofpaires)
  k=0
  for i in range (0, numofline-1):
    if basket[i] != '':
        #print (basket[i])
      for j in range (i+1 ,numofline):
        relativeTime.append(float((basket[j].split())[1])- float((basket[i].split())[1]))
        #relativeTime[k]=CalculateRelTime((basket[j].split())[1], (basket[i].split())[1])
        #print (relativeTime[k])
        paired.append(str((basket[i].split())[0])+ '->'+ str((basket[j].split())[0]))
        k=k+1
  ETpaired=["%s%   0f" % t for t in zip(paired, relativeTime)]
#print (paired)
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

def main(InputTrace):
    AlarmAbnormality()
  
#readInputTETrace()
#sortinvariants()
  ################################################################################
if __name__ == '__main__':
    main(sys.argv[1])


