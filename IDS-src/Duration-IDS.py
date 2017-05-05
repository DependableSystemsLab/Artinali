#! /usr/bin/env python3
###### THIS SCRIPT FINDS THE SUSPICIOUS TIME DURATION FOR ALL GIVEN EVENTS OF INPUT TRACES. ######
###### WRITTEN BY MARYAM RAIYAT ALIABADI#################################################
###### 12TH JULY 2016##############################################################################################
import sys, os
import shutil, errno
import subprocess
Inv=os.path.basename(sys.argv[1])
InputTrace=os.path.basename(sys.argv[2])
############################################################################
def readInputTrace():
    global InputTrace, Inv, lines1, lines2, in1, in2, DataInv, trace, baskets
    f = open('DurationAbnormality.txt', 'w').close()
    ###### taking the data invariant file ########################################
    lines1 = open(Inv).read().splitlines()
    #### removing empty members from list############################
    lines1= [x for x in lines1 if x]
    
    ##### taking the runtime trace ##############################################
    lines2 = open(InputTrace).read().splitlines()
    lines2= [x for x in lines2 if x]
    return lines1 , lines2
###############################################################################


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
    
    Duration, in2 = readInputTrace()
    baskets= [i for i in split_seq(in2,":::")]
    abnormality=[]
    Duration= [x for x in Duration if x]
    for i in range (0, len (baskets)):
        basket=baskets[i]
        group= GroupEvents(basket)
        DELTA= CalDuration(group)
            # DELTA=[item for sublist in DELTA for item in sublist]
        DELTA= [x for x in DELTA if x]
        print ("DELTA", DELTA)
        #print ("duration", Duration)
        for j in range(0, len(Duration)):
            #print ("duration", Duration[j].split())
            for k in range (0 , len(DELTA)):
                shorter=0
                longer=0
                if DELTA[k].split()[0]==Duration[j].split()[0]:
                    print ("debug")
                    print (float(DELTA[k].split()[1]))
                    #print (float(Duration[j].split()[1]))
                    if  float(DELTA[k].split()[1])<=float(Duration[j].split()[2]) :
                        if float(DELTA[k].split()[1])>=float(Duration[j].split()[4]) :
                            print ("in normal range")
                        else:
                            shorter=1
                            print ("abnormality in lowerband", i, DELTA[k])
                    else:
                        longer=1
                        print ("abnormality in upperband", i, DELTA[k])
                        
                if shorter==1 or longer==1 :
                    abnormality.append(i)
                    abnormality.append(DELTA[k].split())
                    abnormality.append(Duration[j])
                    abnormality.append('&&')

    abnormality= [i for i in split_seq(abnormality,"&&")]

######### removing duplicated lists from a list#########
    for n in range (0, (len(abnormality)-1)):
        if abnormality[n]==abnormality[n+1]:
            abnormality[n]=''
    print ("ab", abnormality)
########## adding trace information####################
    for n in range (0, len(abnormality)):
        abnormality[n][0]= [" Trace # : "+ str(abnormality[n][0])]
        abnormality[n][0]=''.join(abnormality[n][0])
        abnormality[n][1]= ["Anomalous duration : "+ str(': '.join(abnormality[n][1]))]
        abnormality[n][1]=''.join(abnormality[n][1])
        abnormality[n][2]= ["Violated invariant : "+ str(abnormality[n][2])]
        abnormality[n][2]=''.join(abnormality[n][2])
    
    ######### write the abnormalities in a file############
    for n in range (0, len(abnormality)):
        ABnumber= ["Abnormality ",str (n+1),". "]
        ABnumber=''.join(ABnumber)
        f = open('DurationAbnormality.txt', 'a')
        f.write( '  '.join(map(lambda x: str(x), [str(ABnumber)])) + "\n")
        f.write( '\n '.join(map(lambda x: str(x), abnormality[n])) + "\n" +"\n")
        f.close()


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
    #print ("delta", delta)
    return delta




############################################################################
def main(InputTrace):
    AlarmAbnormality()
################################################################################
if __name__ == '__main__':
        main(sys.argv[1])


