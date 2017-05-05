
======
Pre-requisites
  1. Python 3
  2. 64 bit Machines with 64 bit Linux/OS X.

======
Installation
  A. Install Python 3

  B. Download ARTINALI
    	
  C. Testing ARTINALI
    1.You can use CustomAPI functions to instrument the example programs in /ARTINALI/test_suite/PROGRAMS/ and collect traces after running the code. As a result, three log files including DELOG, TELOG and DurationLOG will be generated.
    or
    2. You can directly use the collected traces from /ARTINALI/CPS-traces/ to test ARTINALI.

    Example program: SEGMeter
      1. Copy ARTINALI-src/ to your project directory and change to ARTINALI-src/CPS-traces/SEGMETER/ directory. 

      2. Run python <ARTINALIsrc_ROOT>/Invariant-Inf/DEMiner.py DELOG-SEGMeter.txt
      You should be able to see DEInv.txt 

      3. Run python <ARTINALIsrc_ROOT>/Invariant-Inf/TEMiner.py TELOG-SEGMeter.txt
      You should be able to see TEInv.txt 

      4. Run python <ARTINALIsrc_ROOT>/Invariant-Inf/DurationMiner.py duraion-SEGMeter.txt
      You should be able to see TDInv.txt  


   You may want to compare the result of steps 2-4 with invariants reference in ARTINALI-src/Invariants/SEGMeter/

  D. Testing IDS
   
    1. Run python <ARTINALIsrc_ROOT>/IDS-src/DE-IDS.py DEInv.txt faulty-DELOG-SEGMeter
      You should be able to see DataAbnormality.txt 
  
    2. Run python <ARTINALIsrc_ROOT>/IDS-src/TE-IDS.py TEInv.txt faulty-TELOG-SEGMeter
      You should be able to see TimeAbnormality.txt 
 
    3. Run python <ARTINALIsrc_ROOT>/IDS-src/Duration-IDS.py DEInv.txt faulty-duration-SEGMeter
      You should be able to see DurationAbnormality.txt 
 
     
======