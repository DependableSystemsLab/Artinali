

function DATALOG(MyVariable)
    local  value= _G[MyVariable] 
        
    f=io.open("DELOG.txt","a")
        if value ~= nil then
            f:write( MyVariable, " = ")
            local vtype = type( value )
            if vtype == 'string' then
                f:write( string.format( "%q", value ) )
            elseif vtype == 'number' or vtype == 'boolean' then
                f:write( tostring( value ) )
            else
                -- do nothing - unsupported type
            end
        else
           f:write( MyVariable, " = nil ")
        end
    f:write( "\n" )
    f:close() 
    print ( MyVariable, "=", value, "\n")
   
end    

command= 'all_nodes(start_data)'
DATALOG ("command")