/* secondDLL.cpp (C) 2016 by Maryam Raiyat Aliabadi
 * gcc -Wall -shared -fPIC -o CDataLog.so -I/usr/include/lua5.1 -llua5.1 secondDLL.cpp
 * Note the word "CTimeLog" matches the string after the underscore in
 * function luaopen_CDataLog(). This is a must.
 * The -shared arg lets it compile to .so format.
 * The -fPIC is for certain situations and harmless in others.
 * On your computer, the -I and -l args will probably be different.
*/

#include <lua5.1/lua.h>                               /* Always include this */
#include <lua5.1/lauxlib.h>                           /* Always include this */
#include <lua5.1/lualib.h>                            /* Always include this */
#include <sys/time.h>
#include <string>
#include <stdio.h>
#define DATALOG(name1) datalog(#name1 ,(name1))
template <typename mytype>

static int EVENTLOG(lua_State *L){                      /* Internal name of func */ 
          int number = lua_tonumber(L, -1);             /* Get the number arg */
          std::string Event = lua_tostring(L, -1);      /* Get the string arg */
          std::cout << "event = " << system_call << std::endl;
          std::cout << "number of data variables is : "<<  _Num_of_variables<< std::endl;
          lua_pushnumber(L, number);         /* Push the return */ 
          lua_pushstring(L, Event);           /* Push the return */ 
         return 2;                             /* two return values */
}  



static int datalog(lua_State *L){                      /* Internal name of func */ 
          int number = lua_tonumber(L, -1);             /* Get the number arg */
          std::string Event = lua_tostring(L, -1);      /* Get the string arg */
          std::cout << name1 << "=" << value1<< std::endl;
          lua_pushnumber(L, number);         /* Push the return */ 
          lua_pushstring(L, Event);           /* Push the return */ 
         return 2;                             /* two return values */
}    
//

/* Register this file's functions with the
 * luaopen_libraryname() function, where libraryname
 * is the name of the compiled .so output. In other words
 * it's the filename (but not extension) after the -o
 * in the cc command.
 *
 * So for instance, if your cc command has -o TIMELOG.so then
 * this function would be called luaopen_CTimeLog().
 *
 * This function should contain lua_register() commands for
 * each function you want available from Lua.
 *
*/
int luaopen_CDataLog(lua_State *L){
	lua_register(
			L,               /* Lua state variable */
			"Dlog",         /* func name as known in Lua */
			datalog      /* func name in this file */
			);  
        lua_register(
			L,               /* Lua state variable */
			"Elog",         /* func name as known in Lua */
			EVENTLOG     /* func name in this file */
			);  
	return 0;
}
