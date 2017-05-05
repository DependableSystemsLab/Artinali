

 -- function closures are powerful

-- traditional fixed-point operator from functional programming

function EVENTLOG(system_call, _NumofVar)
    event=system_call
    print ("Event: ",system_call , "  _NumberOfExpectedDataVariables: ", _NumofVar, "\n") 
    f=io.open("DELOG.txt","a")
    f:write( "\nEvent: ",system_call , "\n")
    f:close() 
end
