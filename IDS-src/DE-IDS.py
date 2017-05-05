#! /usr/bin/env python3
###### THIS SCRIPT FINDS THE SUSPICIOUS DATA FOR ALL GIVEN EVENTS OF INPUT TRACES. ######
###### WRITTEN BY MARYAM RAIYAT ALIABADI#################################################
###### 6TH JULY 2016#####################################################################

import sys, os
import shutil, errno
import subprocess


script_path = os.path.realpath(os.path.dirname(__file__))
Inv = os.path.basename(sys.argv[1])
InputTrace = os.path.basename(sys.argv[2])
basedir= os.getcwd()

#############################################################################

def readInputTrace():
  global InputTrace1, Inv, lines1, lines2, in1, in2, DataInv, trace, baskets
  f= open('DataAbnormality.txt', 'w').close()
  ###### taking the data invariant file ########################################
  lines1 = open(Inv).read().splitlines()
  #### removing empty members from list############################
  lines1= [x for x in lines1 if x]
  ####removing whitespace from string objects######################
  for i in range (0 , len (lines1)):
    lines1[i] = ''.join(lines1[i].split())
    lines1[i].replace(" ", "")
  ############ separating invariants and coincidences##############
  sets = [i for i in split_seq(lines1,"::::::")]
  Inv_set=[]
  coin_set=[]
  Inv_set.append (sets[0])
  Inv_set=[item for sublist in Inv_set for item in sublist]
  coin_set.append(sets[1])
  coin_set=[item for sublist in coin_set for item in sublist]
  print(Inv_set)
  print (coin_set)

  ##### taking the runtime trace ##############################################
  lines2 = open(InputTrace).read().splitlines()
  lines2= [x for x in lines2 if x]
  for i in range (0 , len (lines2)):
    lines2[i] = ''.join(lines2[i].split())
    lines2[i].replace(" ", "")
  return Inv_set, coin_set, lines2


##### putting every event with the related data in one list##################
def DataEventGrouping (input):
    MergedLine= []
    Eindex=[]
    temp=[]
    for i in range (0, len(input)):
        uline= input[i].split()
        j=0
        if  input[i][0:6]== "Event:":
            Eindex.insert(j,i)
            Eindex.sort()
        j=j+1
    for j in range (1, len(Eindex)):
        MergedLine= ['  '.join( input [Eindex[j-1]: Eindex[j]] )]
        temp= temp +MergedLine
        del MergedLine[:]
        next=Eindex[j]
    MergedLine= MergedLine +['  '.join(  input[next: len (input) +1])]
    temp= temp+MergedLine
                #print ("temp: " , temp)
    del input [:]
    input = temp
#print (temp)
    return temp
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
############################################################################
def intersect(a,b):
    #a= ['Event:send()', 'd1=true', 'd2=all_data', 'd3=time_out, d3=time_in']
    #b= ['Event:send()', 'd1=true', 'd2=all_data', 'd3=time_out']
    c=[]
    merge=[]
    for element in a:
        parts = element.split(',')
    a=a+parts
#print (a)
    if  a[0]==b[0]:
        del merge[:]
        for p in range (0, len(a)):
            for k in range (0, len (b)):
                merge.append(list(set(a[p].split()) & set (b[k].split())))
        merge=[item for sublist in merge for item in sublist]
        merge = [x for x in merge if x != []]

        c.append(merge)
    c = sorted(set(c[0]))
#print ("c is :", c)
    return c


#############################################################################
def AlarmAbnormality():
    
    in1, in0, in2= readInputTrace()
    DataInv= DataEventGrouping (in1)
    Coincident=DataEventGrouping (in0)
    DataInvClass=[[] for i in range (len(DataInv)) ]
    baskets= [i for i in split_seq(in2,":::")]
    Con_abnormality=[]
    abs_abnormality=[]
    print ("number of baskets", len (baskets))
    for i in range (0, len (baskets)):
        basket=baskets[i]
        print ("len of basket", len (basket))
        trace= DataEventGrouping (basket)
        print ("number of trace", len (trace))
        traceClass=[[] for k in range (len(trace)) ]
        for m in range (0, len(trace)):
            traceClass[m]=trace[m].split()
            for n in range (0, len(DataInv)):
                DataInvClass[n]=DataInv[n].split()
                print ("invar", DataInvClass[n])
                if (DataInv[n].split()[0]== trace[m].split()[0]) :
                    for k in range (1,len(DataInv[n].split())):
                        print ("inv", DataInv[n].split())
                        print ("trace", trace[m].split())
                        print (n, k)
                        string=list(DataInv[n].split()[k])
                        index=string.index("=")
                        name1=string[:index]
                        name1= ''.join(name1)
                        value1=string[index+1:]
                        value1= ''.join(value1)
                        for p in range (1, len(trace[m].split())):
                            flag=0
                            string2=list(trace[m].split()[p])
                            index2=string2.index("=")
                            name2=string2[:index2]
                            name2= ''.join(name2)
                            value2=string2[index2+1:]
                            value2= ''.join(value2)
                            if (name1 == name2 ):
                                flag=1
                                if value2 in value1:
                                    print ("absolute normality")
                                else:
                                    print (" conditional normality seen in trace # ",i, "is: ", trace[m].split()[p])
                        ################################
                                    Con_abnormality.append(i)
                                    Con_abnormality.append(m)
                                    Con_abnormality.append(p)
                                    Con_abnormality.append(trace[m].split())
                                    Con_abnormality.append('&&')
                                    print (Con_abnormality)
                       
                                    for s in range (0, len (Coincident)):
                                        if (Coincident[s].split()[0]== trace[m].split()[0]) :
                                            for t in range (1,len(Coincident[s].split())):
                                                string0=list(Coincident[s].split()[t])
                                                index0=string.index("=")
                                                name0=string[:index0]
                                                name0= ''.join(name0)
                                                value0=string[index0+1:]
                                                value0= ''.join(value0)
                                                if (name2==name0):
                                                    if value2 in value0:
                                                        print("might be")
                                                    else:
                                                        print("absolute abnormality")
                                                        abs_abnormality.append(i)
                                                        abs_abnormality.append(m)
                                                        abs_abnormality.append(p)
                                                        abs_abnormality.append(trace[m].split())
                                                        abs_abnormality.append(DataInv[n])
                                                        abs_abnormality.append('&&')
                        #################################
                            if (flag ):
                                break
    abs_abnormality= [i for i in split_seq(abs_abnormality,"&&")]
    ######### removing duplicated lists from a list#########
    for n in range (0, (len(abs_abnormality)-1)):
        if abs_abnormality[n]==abs_abnormality[n+1]:
            abs_abnormality[n]=''
    #### removing empty members from list############################
    abs_abnormality= [x for x in abs_abnormality if x]
    ######### flattening a list#############################
    #var_name[i]=[item for sublist in var_name[i]for item in sublist]
    print (" abs_abnormality", abs_abnormality)
    ########## adding trace information####################
    for n in range (0, len(abs_abnormality)):
        abs_abnormality[n][0]= [" Trace # : "+ str(abs_abnormality[n][0])]
        abs_abnormality[n][0]=''.join(abs_abnormality[n][0])
        abs_abnormality[n][2]= ["Anomalous value : "+ str(abs_abnormality[n][3][abs_abnormality[n][2]])]
        abs_abnormality[n][2]=''.join(abs_abnormality[n][2])
        abs_abnormality[n][3]=' , '.join(abs_abnormality[n][3])
        abs_abnormality[n][1]= ["Line : "+ str(abs_abnormality[n][3])]
        abs_abnormality[n][1]=''.join(abs_abnormality[n][1])
        abs_abnormality[n][4]=abs_abnormality[n][4].split()
        abs_abnormality[n][4]= ["Violated invariant : "+ str(', '.join(abs_abnormality[n][4]))]
        abs_abnormality[n][4]=' '.join(abs_abnormality[n][4])
        abs_abnormality[n].pop(3)

    ######### write the abnormalities in a file############
    for n in range (0, len(abs_abnormality)):
        ABnumber= ["Abnormality ",str (n+1),". "]
        ABnumber=''.join(ABnumber)
        f = open('DataAbnormality.txt', 'a')
        f.write( '  '.join(map(lambda x: str(x), [str(ABnumber)])) + "\n")
        f.write( '\n '.join(map(lambda x: str(x), abs_abnormality[n])) + "\n" +"\n")
        f.close()

############################################################################
def main(InputTrace):
    AlarmAbnormality()
    #in1, in2= readInputTrace()
# DataInv= DataEventGrouping (in1)
    #for j in range

################################################################################
if __name__ == '__main__':
    main(sys.argv[1:])



