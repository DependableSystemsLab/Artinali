#!/usr/bin/lua
-- TIMELOG.lua (lua) 2016 by Maryam Raiyat Aliabadi.
-- The TIMELOG module collects the timestamp of input event in microsecond resolution.

function TIMELOG(event)
    require("CTimeLog")                               -- CTimeLog.so is a shared library comming from C.
    microsec, curtime= MTime()
    print (curtime,microsec, " ", event)
    f=io.open("TELOG.txt","a")
    f:write (event, "  ", curtime,microsec , "\n")   -- time stamps are logged into the timelog.txt file.
    f:close()
end

