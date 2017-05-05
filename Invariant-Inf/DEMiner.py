#! /usr/bin/env python3
###### THIS SCRIPT FINDS THE DATA INVARIANTS FOR ALL GIVEN EVENTS OF INPUT TRACES. ##########################################
###### WRITTEN BY MARYAM RAIYAT ALIABADI #####################################################################################
###### 3rd JUNE 2016##########################################################################################################

import sys, os
import shutil, errno
import subprocess


script_path = os.path.realpath(os.path.dirname(__file__))
InputTrace = os.path.basename(sys.argv[1])
basedir= os.getcwd()
############################################################################

def checkInputTrace():
	#Check for Input Trace's presence
  global cOpt
  srcpath = os.path.dirname(options["source"])
  try:
    f = open(os.path.join(srcpath, 'trace.txt'), 'r')
  except:
    print("ERROR: No trace.txt file in the %s directory." % srcpath)
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

def readInputTrace():
  global InputTrace,C, classes, numofclass, Var_names ,s, Lines, lines, baskets, newbasket,VN
  f= open('DEInv.txt', 'w').close()
  
  lines = open(InputTrace).read().splitlines()
  #### removing empty members from list############################
  lines= [x for x in lines if x]
  #print (lines)
  ####removing whitespace from string objects######################
 
  for i in range (0 , len (lines)):
    lines[i] = ''.join(lines[i].split())
    # print ("here", lines[i])
    lines[i].replace(" ", "")
  # print (lines[i])
  
  ######deviding log into baskets (different executions)############
  baskets= [i for i in split_seq(lines,":::")]
  DEinvariants= [[] for i in range(len(baskets))]
  newbasket=[[] for i in range(len(baskets))]
  SNames=[[] for i in range(len(baskets))]
  final=[]
  temp3=[]
  for i in range (0, len (baskets)):
    basket=baskets[i]
    newbasket[i], SNames[i]=ChangeFormat(basket)
        #SNames[i]=[item for sublist in SNames[i] for item in sublist]
    my_set = set(tuple(x) for x in SNames[i])
    SNames[i] = [ list(x) for x in my_set ]
    my_set = set(tuple(x) for x in SNames[i])
    SNames[i] = [ list(x) for x in my_set ]
#  print ("snames", SNames[i])
#print (DEinvariants[i])
  DE=[[] for i in range(len(baskets))]
  VN=[[] for i in range(len(baskets))]
  for i in range (0, len(newbasket)):
      # print ("newbasket[i] is : ", newbasket[i])
    newbasket[i]=[j for j in split_seq(newbasket[i],"&&")]
#print ("newbasket", newbasket)
  for i in range (0, len(newbasket)-1):
    DE[i],DE[i+1]=FindFrequentitemSet(newbasket[i], newbasket[i+1])
    VN[i], VN[i+1]=FindFrequentitemSet(SNames[i], SNames[i+1])
    my_set = set(tuple(x) for x in VN[i])
    VN[i] = [ list(x) for x in my_set ]
# print ("vn", VN[i])
  VN=[item for sublist in VN for item in sublist]
  my_set = set(tuple(x) for x in VN)
  VN = [ list(x) for x in my_set ]

  for i in range (0, len (DE)):
    print ("DE", DE)

  final=list (DE[0])
  for i in range (0, len (newbasket)-1):
    union_item, common_item, delta_item=union (final, DE[i+1])
    #set1=list(common_item)
    intersected_inv=AttachVariableNames(common_item)
  for n in range (0, len(intersected_inv)):
    DEnumber= ["D|E Invariant ",str (n+1),". "]
    DEnumber=''.join(DEnumber)
    f = open('DEInv.txt', 'a')
    #f.write( '  '.join(map(lambda x: str(x), [str(DEnumber)])) + "\n")
    f.write( '\n '.join(map(lambda x: str(x), intersected_inv[n])) + "\n" +"\n")
    f.close()
  f = open('DEInv.txt', 'a')
  f.write("::::::"+"\n"+"\n")
  f.close()
  Coincidence=AttachVariableNames(delta_item)
  for n in range (0, len(Coincidence)):
    DEnumber= ["Coincidence ",str (n+1),". "]
    DEnumber=''.join(DEnumber)
    f = open('DEInv.txt', 'a')
    # f.write( '  '.join(map(lambda x: str(x), [str(DEnumber)])) + "\n")
    f.write( '\n '.join(map(lambda x: str(x), Coincidence[n])) + "\n" +"\n")
    f.close()




################################################################################################
def AttachVariableNames(final):
  for n in range (0, len(final)):
      for m in range (0, len(VN)):
          if VN[m][0] == final[n][0]  :
              for k in range (1, len(final[n])):
                  if final[n][k]!='':
                      final[n][k]= '='.join([VN[m][k], final[n][k]])
  for i in range (0, len(final)):
      final[i] = [x for x in final[i] if x]
      if len(final[i])==1:
          print ("debug")
          final[i]=''
  final= filter(None, final)
  for n in range (0, len(final)):
      final[n]= [w.replace(' ', ' , ') for w in final[n]]
  print ( " replacement" ,final)
  return (final)

########################################
def FindFrequentitemSet(A,B):
    #A=[['Event:send()', 'd1=true', 'd2=all_data', 'd3=time_out'], ['Event:recv()', 'd1=false', 'd2=nil', 'd3=closed'], ['Event:read()', 'd1=true', 'd5=5', 'd6=8.5']]
    # B=[['Event:send()', 'd1=true', 'd2=all_data', 'd3=time_out'], ['Event:recv()', 'd1=false', 'd2=abc , d2=nil', 'd3=closed']]
    AA=[]
    BB=[]

    for m in range (0, len(A)):
        for n in range (0 , len (B)):
            if A[m][0]==B[n][0]:
                AA.append(A[m])
                BB.append(B[n])
    return AA, BB

  ###########################################################################
def union (a,b):
    #a=[['Event:send()', 'true', 'all_data', 'time_out'], ['Event:recv()', 'false', 'nil', 'closed']]
    #b=[['Event:recv()', 'false', 'abc  nil', 'closed'],['Event:send()', 'true', 'all_data', 'time_out']]
    #a=[['Event:add_node', 'farid'], ['Event:get_node_atoms', '"(p_160.90)(e_10.64)"', 'farid'], ['Event:determine_node_name', '"(p_1 45.68)(e_1 0.44)(p_2 19.03)(e_2 0.22)(p_3 19.03)(e_3 0.21)(p_4 19.03)(e_4 0.22)(p_5 19.03)(e_5 0.21)(p_6 19.03)(e_6 0.21)(p_7 19.03)(e_7 0.24)(p_8 0.00)(e_8 0.00)(p_1 41.87)(e_1 0.44)(p_2 22.84)(e_2 0.22)"', 'farid']]
    #b=[['Event:add_node', 'farid'], ['Event:get_node_atoms', '(p_164.71)(e_10.64)', 'farid'], ['Event:determine_node_name', '"(p_1 45.68)(e_1 0.44)(p_2 19.03)(e_2 0.22)(p_3 19.03)(e_3 0.21)(p_4 19.03)(e_4 0.22)(p_5 19.03)(e_5 0.21)(p_7 19.03)(e_6 0.21)(p_7 19.03)(e_7 0.24)(p_8 0.00)(e_8 0.00)(p_1 41.87)(e_1 0.44)(p_2 22.84)(e_4 0.22)"', 'farid']]
    temp=[[] for i in range(len(a))]
    merged=[]
    shared=[]
    delta=[]
    for n in range (0, len(a)):
        for m in range (0 , len (b)):
            # print ("a[n]", a[n])
            # print ("b[m]", b[m])
            if a[n][0]==b[m][0] :
                #print ("debug")
                merged.append(a[n][0])
                shared.append(a[n][0])
                delta.append(a[n][0])
                for k in range (1, len(a[n])):
                    pure_c=list (set (a[n][k].split()).union(b[m][k].split()))
                    pure_c=' '.join (pure_c)
                    pure_int=list (set (a[n][k].split()).intersection(b[m][k].split()))
                    pure_int=' '.join (pure_int)
                    print ("pure-int", pure_int)
                    #pure_delta=list (set (pure_int.split()).intersection(pure_c.split()))
                    pure_delta=[item for item in pure_c.split() if item not in pure_int.split()]
                    print ("pure-delta", pure_delta)
                    pure_delta=' '.join (pure_delta)
                    merged.append (pure_c)# insert (k+1,pure_c)
                    shared.append (pure_int)
                    delta.append (pure_delta)
                #delta= [x for x in delta if x]
                merged.append("&&")
                shared.append("&&")
                delta.append("&&")
    merged=[j for j in split_seq(merged,"&&")]
    shared=[j for j in split_seq(shared,"&&")]
    delta=[j for j in split_seq(delta,"&&")]
#delta= [x for x in delta if x]
    print ("union",merged)
    print ("intersection",shared)
    print ("delta", delta)
    return merged , shared, delta
#############################################################################
def intersect(a,b):
    #a=[['Event:send()', 'd1=true', 'd2=all_data', 'd3=time_out'], ['Event:recv()', 'd1=false', 'd2=nil', 'd3=closed']]
  #b=[['Event:recv()', 'd1=false', 'd2=abc , d2=nil', 'd3=closed'],['Event:send()', 'd1=true', 'd2=all_data', 'd3=time_out']]
  c=[]
  merge=[]
  for k in range (0, len(a)):
      for p in range (0, len(b)):
          if a[k]==b[p]:
              c.append(a[k])
              sign=1
          elif  a[k][0]==b[p][0] :
              del merge[:]
              for m in range (0, len(a[k])):
                  for n in range (0, len (b[p])):
                      merge.append(list(set(a[k][m].split()) & set (b[p][n].split())))
              merge=[item for sublist in merge for item in sublist]
              #print ("merge2 is" ,merge)
              merge = [x for x in merge if x != []]
              #print ("merge3 is" , len(merge), merge)
          c.append(merge)
          sign=1
          print ( "c1 is ", c)
          print (k, p)
          print ( "c2 is ", c)
              #if sign :
              #  break
      print ( "c3 is ", c)
  print ( "c4 is ", c)
  return c

############################################################################
def flatten(x):
  if not isinstance(x,list):
    return x
  elif len(x) is 0:
    return []
  elif isinstance(x[0],list):
    return flatten(x[0]) + flatten(x[1:])
  else:
    return [x[0]] + flatten(x[1:])

  #################START OF FORMAT CHANGE##################################
def ChangeFormat(lines):
  global var_name
  MergedLine= []
  Eindex=[]
  temp=[]
  
  lines = [x for x in lines if x]
  for i in range (0, len(lines)):
    uline= lines[i].split()
    j=0
    if  lines[i][0:6]== "Event:":
        #lines[i]=lines[i][6:]
      Eindex.insert(j,i)
      Eindex.sort()
    j=j+1
  for j in range (1, len(Eindex)):
    MergedLine= ['  '.join( lines [Eindex[j-1]: Eindex[j]] )]
    temp= temp +MergedLine
    del MergedLine[:]
    next=Eindex[j]

  MergedLine= MergedLine +['  '.join(  lines [next: len (lines) +1])]
  temp= temp+MergedLine
#print ("temp: " , temp)
  del lines [:]
  lines = temp
  # return temp
  print ("format change is done")
###########################################################################

##****************####3
  numoflines=len (lines)
  C=[]

  for i in range (0, numoflines):
    if lines[i] != '':
      sline= lines[i].split()
      numofDataVar=len(sline)
      C.append(sline[0])
  #####removing duplication###########
  C = list(set(C))
# print (C)
  numofclass=len(C)
  newlines=[[] for i in range (len(lines))]

  
  ####classify traces based on the events#########
  numofDataVariables=[[] for i in range(numofclass)]
  classes=[[] for i in range(numofclass)]
  for j in range (0, numofclass) :
    for i in range (0, numoflines) :
      sline= lines[i].split()
      if C[j] in sline :
        classes[j].append(lines[i])
    numofDataVariables[j]=len(classes[j][0].split())
#print ("numofdatavar",numofDataVariables[j])
#print ("classes ARE", classes)

  print("classification is done!")
  #print ("lines", lines)
### removing the name of variables####
  CLA=[[] for i in range (len(lines))]
  pure_class=[[] for i in range(numofclass)]
  var_name=[[] for i in range(numofclass)]
  splitted_name=[[] for i in range(numofclass)]
  for p in range (0, numofclass):
      CLASSES=[[] for i in range (len(classes[p]))]
      for k in range (0,len (classes[p])):
          # print (len(classes[p]))
          
          CLASSES[k]=classes[p][k].split()
      # print ("CLASSES[k] ",CLASSES[k])
      CLA[p] = [x for x in CLASSES if x != []]
# print ("CLA[p] ",CLA[p])
  CLA = [x for x in CLA if x != []]
  #print ("CLA.. ",CLA)################ CLA is classes and just the format is changed to be acceptable to SplitAllnames function
  for i in range (0, numofclass):
      pure_class[i], var_name[i] =SplitAllNames(CLA[i])
      var_name[i] = [x for x in var_name[i] if x != []]
      ######### removing duplicated lists from a list#########
      b_set = set(tuple(x) for x in var_name[i])
      var_name[i] = [ list(x) for x in b_set ]
      ######### flattening a list#############################
      var_name[i]=[item for sublist in var_name[i]for item in sublist]
    
 #### merging the data viariables of the same class########################
  DEinvariant=[]
  temp2=[]
  MergedData=[]
  #print (pure_class)
  for i in range (0, len (pure_class)):
    print ("pure_class[i]", pure_class[i])
    prim= pure_class[i][0]
    for j in range (0, len (pure_class[i])-1):
      
      del  MergedData[:]
      for k in range (0, len(pure_class[i][j])):
          
        Mergedobj=list (set (prim[k].split()).union(pure_class[i][j+1][k].split()))
        Mergedobj=' '.join (Mergedobj)
        MergedData.append (Mergedobj)# insert (k+1,pure_c)
        print ("mergeddata",MergedData)
      prim=list (MergedData)

#print ("prim",prim)
      print (i,j,k)
      #print ("pure_class[i][j] down", pure_class[i][j])
    prim.append("&&")
# MergedData=[j for j in split_seq(MergedData,"&&")]
#print ("mergeddata", MergedData)
    DEinvariant=DEinvariant+prim
    #print (DEinvariant)
  return DEinvariant, var_name
        #print (len(final))
#del newbasket [:]
###########################

##########################################################################
def SplitVariableNames(s):
    #s= ['send' , 'd1=4' ,'d2=6']
    #s=['send', 'get_segmeter_data=true', 'command=\xe2\x80\x9c(all_nodes(start_data))\xe2\x80\x9d', 'partial=nil', 'status=nil', 'validated_message=nil']
    name_list=[[] for i in range (len(s))]
    # s=s.split()
    for i in range (1, len(s)):
        string=list(s[i])
        index= string.index("=")
        name_list[i]=string[:index]
        s[i]=string[index+1:]
    name_list = [x for x in name_list if x != []]
    for i in range (0, len(s)):
        s[i]=''.join(s[i])
    for i in range (0, len (name_list)):
        name_list[i]= ''.join(name_list[i])
    name_list.insert(0,s[0])
#print ("name_list", name_list)
    return s, name_list

########################################


def ExtractNames(s):
#s= ['send()', 'd1=true', 'd2=all_data', 'd3=time_out']
    name_list=[[] for i in range (len(s))]
    for i in range (1, len(s)):
        string=list(s[i])
        index= string.index("=")
        name_list[i]=string[:index]
    name_list = [x for x in name_list if x != []]
    for i in range (0, len (name_list)):
        name_list[i]= ''.join(name_list[i])
    #print (name_list)
    return (name_list)


 ##############################################################################

def SplitAllNames(Lines):
    #Lines=[['Event:send()', 'd1=true', 'd2=all_data', 'd3=time_out'], ['Event:recv()', 'd1=false', 'd2=nil', 'd3=closed']]
    newLine=[[] for i in range (len(Lines))]
    names=[[] for i in range (len (Lines))]
    for i in range (0, len (Lines)):
        newLine[i], names[i] = SplitVariableNames(Lines[i])#.split())
    #newLine[i]='  '.join(newLine[i])
    
    #print (newLine, names)
    return newLine, names
##############################################################################

def DataMerging():
	myClass={}
	for j in range (0, numofclass):
		myClass[j]=[]
		numofclassmates= len(classes[j])
		smate0=classes[j][0].split()
		for i in range (1, numofclassmates):
			smate1=classes[j][i].split()
			
			smate0= [str(smate0[k]) + "," + str(smate1[k]) for k in range (len(smate0))] 
			myClass[j]=smate0
	

############################################################################
def main(InputTrace):
    #checkInputTrace()
  readInputTrace()
#union ()
#SplitAllNames()
# intersect()
#FindFrequentitemSet()
# ChangeFormat(lines)
# GroupDataPerEvent ()
################################################################################
if __name__ == '__main__':
    main(sys.argv[1])



