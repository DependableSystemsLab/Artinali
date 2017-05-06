
======
Pre-requisites
  1. Python 2
  2. 64 bit Machines with 64 bit Linux/OS X.

======
Installation
  A. Install Python 2 and check whether the "python" command invokes Python by running "python --verbose". If Python 3 is invoked, then for all steps described below, use command "python2" instead of "python" to force the usage of Python 2.

  B. Clone the ARTINALI repository (git clone https://github.com/karthikp-ubc/Artinali.git). In the steps outlined below, "ARTINALI-src" refers to the source directory of your ARTINALI working copy.
    	
  C. Testing ARTINALI
    1.You can use CustomAPI functions to instrument the example programs and collect traces after running the code. As a result, three log files including DELOG, TELOG and DurationLOG will be generated. You can access the source code of our example programs (SEGMeter and OpenAPS) by cloning the following repositories:
    (a) https://github.com/samotage/Aiko.git
    (b) https://github.com/openaps/oref0.git
 
    or
    2. You can directly use the collected traces from /ARTINALI/CPS-traces/ to test ARTINALI.

    Example program: SEGMeter
      1. Change to ARTINALI-src/CPS-traces/SEGMETER/ directory. 

      2. Run python <ARTINALIsrc_ROOT>/Invariant-Inf/DEMiner.py DELOG-SEGMeter.txt
      DEMiner.py takes a sequence of traces that include the instrumented events and their associated data variables, and mines data invariants that hold within every event.You should be able to see the result in DEInv.txt 

      3. Run python <ARTINALIsrc_ROOT>/Invariant-Inf/TEMiner.py TELOG-SEGMeter.txt
      TEMiner.py takes a sequence of traces that include the instrumented events and the time stamps after events, and mines the patterns of normal order of events along with their time boundaries and their occurrence frequency.You should be able to see the result in TEInv.txt 

      4. Run python <ARTINALIsrc_ROOT>/Invariant-Inf/DurationMiner.py duraion-SEGMeter.txt
      TEMiner.py takes a sequence of traces that include the instrumented events and the time stamps before and after every event, and mines the time takes that every event is executed. You should be able to see the result in TDInv.txt  


   You may want to compare the result of steps 2-4 with invariants reference in ARTINALI-src/Invariants/SEGMeter/

  D. Testing IDS
   
    1. Run python <ARTINALIsrc_ROOT>/IDS-src/DE-IDS.py DEInv.txt faulty-DELOG-SEGMeter.txt
      DE-IDS.py takes two inputs including Data per Event invariants and the test traces, and reports the abnormal traces. You should be able to see the result in DataAbnormality.txt 
  
    2. Run python <ARTINALIsrc_ROOT>/IDS-src/TE-IDS.py TEInv.txt faulty-TELOG-SEGMeter.txt
      TE-IDS.py takes two inputs including Event per Time invariants and the test traces, and reports the abnormal traces. You should be able to see the result in TimeAbnormality.txt 
 
    3. Run python <ARTINALIsrc_ROOT>/IDS-src/Duration-IDS.py DEInv.txt faulty-duration-SEGMeter.txt
      DE-IDS.py takes two inputs including Duration invariants and the test traces, and reports the abnormal traces. You should be able to see the result in DurationAbnormality.txt 
 
     
======