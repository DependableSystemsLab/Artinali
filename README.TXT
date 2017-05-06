
======
Pre-requisites
  1. Python 2
  2. 64 bit Machines with 64 bit Linux/OS X.

======
Installation
  A. Install Python 2 and check whether the "python" command invokes Python by running "python --verbose". If Python 3 is invoked, then for all steps described below, use command "python2" instead of "python" to force the usage of Python 2.

  B. Clone the ARTINALI repository (git clone https://github.com/karthikp-ubc/Artinali.git). In the steps outlined below, "ARTINALI-src" refers to the source directory of your ARTINALI working copy.
    	
  C. Testing ARTINALI
    1.You can use CustomAPI functions to instrument the example programs in /ARTINALI/test_suite/PROGRAMS/ and collect traces after running the code. As a result, three log files including DELOG, TELOG and DurationLOG will be generated.
    or
    2. You can directly use the collected traces from /ARTINALI/CPS-traces/ to test ARTINALI.

    Example program: SEGMeter
      1. Change to ARTINALI-src/CPS-traces/SEGMETER/ directory. 

      2. Run python <ARTINALIsrc_ROOT>/Invariant-Inf/DEMiner.py DELOG-SEGMeter.txt
      You should be able to see DEInv.txt 

      3. Run python <ARTINALIsrc_ROOT>/Invariant-Inf/TEMiner.py TELOG-SEGMeter.txt
      You should be able to see TEInv.txt 

      4. Run python <ARTINALIsrc_ROOT>/Invariant-Inf/DurationMiner.py duraion-SEGMeter.txt
      You should be able to see TDInv.txt  


   You may want to compare the result of steps 2-4 with invariants reference in ARTINALI-src/Invariants/SEGMeter/

  D. Testing IDS
   
    1. Run python <ARTINALIsrc_ROOT>/IDS-src/DE-IDS.py DEInv.txt faulty-DELOG-SEGMeter.txt
      You should be able to see DataAbnormality.txt 
  
    2. Run python <ARTINALIsrc_ROOT>/IDS-src/TE-IDS.py TEInv.txt faulty-TELOG-SEGMeter.txt
      You should be able to see TimeAbnormality.txt 
 
    3. Run python <ARTINALIsrc_ROOT>/IDS-src/Duration-IDS.py DEInv.txt faulty-duration-SEGMeter.txt
      You should be able to see DurationAbnormality.txt 
 
     
======